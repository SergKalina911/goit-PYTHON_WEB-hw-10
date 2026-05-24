""" Створює міграцію даних з MongoDB Atlas у PostgreSQL через Django ORM.
- Експортує дані з MongoDB Atlas у локальні JSON файли. 
- Імпортує дані з JSON файлів у PostgreSQL, створюючи авторів, цитати та теги.
- Якщо MongoDB Atlas недоступний, використовує локальні JSON файли для міграції. """
import os
import django
import json
import pymongo
from pymongo.errors import ConnectionFailure
from decouple import config

# Ініціалізація Django середовища
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_site.settings")
django.setup()

from quotes.models import Author, Quote, Tag

def export_mongo_to_json():
    """
    Експортує дані з MongoDB Atlas у локальні JSON файли.
    - authors_bs → data/authors.json
    - quotes_bs → data/quotes.json
    """
    MONGO_USER   = config("MONGO_USER")
    MONGO_PASS   = config("MONGO_PASS")
    MONGO_DB     = config("MONGO_DB")
    MONGO_DOMAIN = config("MONGO_DOMAIN")

    # Підключення до Atlas через SRV
    client = pymongo.MongoClient(
        f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_DOMAIN}/{MONGO_DB}?retryWrites=true&w=majority",
        serverSelectionTimeoutMS=5000
    )

    db = client[MONGO_DB]
    client.admin.command("ping")  # перевірка з’єднання

    # Експорт авторів
    authors = list(db.authors_bs.find({}, {"_id": 0}))
    os.makedirs("data", exist_ok=True)
    with open("data/authors.json", "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    # Експорт цитат
    quotes = list(db.quotes_bs.find({}, {"_id": 0}))
    with open("data/quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

    print("✅ Експорт із MongoDB Atlas завершено: створено data/authors.json та data/quotes.json")

def migrate_from_json():
    """
    Імпортує дані з JSON файлів у PostgreSQL через Django ORM.
    - Створює/оновлює авторів з усіма полями.
    - Створює цитати та додає теги.
    - Очищає старі теги, щоб уникнути дублювання.
    """
    try:
        # Імпорт авторів
        with open("data/authors.json", "r", encoding="utf-8") as f:
            authors_data = json.load(f)
            for a in authors_data:
                Author.objects.get_or_create(
                    fullname=a["fullname"],
                    born_date=a.get("born_date", ""),
                    born_location=a.get("born_location", ""),
                    description=a.get("description", "")
                )

        # Імпорт цитат
        with open("data/quotes.json", "r", encoding="utf-8") as f:
            quotes_data = json.load(f)
            for q in quotes_data:
                author, _ = Author.objects.get_or_create(fullname=q["author"])
                quote_obj, _ = Quote.objects.get_or_create(quote=q["quote"], author=author)

                # очищаємо старі теги, щоб уникнути дублювання
                quote_obj.tags.clear()
                for tag in q.get("tags", []):
                    tag_obj, _ = Tag.objects.get_or_create(name=tag)
                    quote_obj.tags.add(tag_obj)

        print("🎉 Дані успішно перенесено з JSON у Postgres")

    except FileNotFoundError as e:
        print(f"❌ Файл не знайдено: {e.filename}. Міграція неможлива.")

def migrate():
    """
    Основна логіка міграції:
    1. Спроба експортувати дані з MongoDB Atlas у JSON.
    2. Імпорт даних із JSON у Postgres.
    3. Якщо Atlas недоступний → fallback на локальні JSON файли.
    """
    try:
        export_mongo_to_json()
        migrate_from_json()
    except ConnectionFailure:
        print("⚠️ Немає зв’язку з MongoDB Atlas. Використовуємо резервні JSON файли.")
        migrate_from_json()

if __name__ == "__main__":
    migrate()
