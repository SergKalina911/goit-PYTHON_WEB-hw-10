# goit-PYTHON_WEB-hw-10

# HW10 – Django + PostgreSQL + MongoDB (міграція даних)

## Опис

У HW09 дані (автори та цитати) зберігалися у MongoDB.  
У HW10 сайт працює на PostgreSQL, тому потрібно перенести дані.

---

## 🚀 Функціонал
- Реєстрація та логін користувачів
- Додавання авторів і цитат (лише для автентифікованих)
- Перегляд авторів та цитат без входу
- Пошук цитат за тегами
- Пагінація (кнопки «Попередня» / «Наступна»)
- Блок «Top Ten Tags»
- Скрапінг цитат із сайту `quotes.toscrape.com`
- Очищення бази кнопкою на головній сторінці
- Міграція даних з MongoDB Atlas у PostgreSQL

---

## 📂 Структура проєкту

```text
goit-PYTHON_WEB-hw-10/
│── README.md              # пояснення, інструкції по запуску
│── .gitignore             # винятки (env, json, кеші, IDE)
│── .env.example           # приклад змінних середовища
│── .env                   # реальні креденшали (у .gitignore)
│── docker-compose.yml     # три сервіси: web, postgres, mongo
│── Dockerfile             # образ для Django + Poetry
│── pyproject.toml         # залежності (django, psycopg2, decouple)
│── poetry.lock
│
│── quotes_site/           # головна папка Django-проєкту
│   ├── manage.py
│   ├── migrate_data.py    # скрипт міграції Mongo → Postgres
│   │
│   ├── quotes_site/       # конфігурація Django
│   │   ├── settings.py    # налаштування (env, postgres, debug)
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   └── quotes/            # додаток з моделями, views, шаблонами
│       ├── models.py      # Author, Quote, Tag
│       ├── views.py       # логіка відображення
│       ├── forms.py       # форми для авторів, цитат, пошуку
│       ├── urls.py        # маршрути
│       ├── admin.py       # реєстрація моделей в адмінці
│       ├── tests.py       # базові тести для моделей і views
│       │
│       ├── templates/quotes/
│       │   ├── base.html            # базовий шаблон
│       │   ├── index.html           # головна сторінка
│       │   ├── author_detail.html   # сторінка автора
│       │   ├── quote_detail.html    # деталі цитати
│       │   ├── quote_list.html      # список цитат (з пагінацією)
│       │   ├── add_author.html      # додавання автора
│       │   ├── add_quote.html       # додавання цитати
│       │   ├── add_tag.html         # додавання тега
│       │   ├── search_author.html   # пошук цитат за автором
│       │   ├── register.html        # шаблон для реєстрації
│       │   └── login.html           # шаблон для входу
│       │
│       └── static/quotes/css/style.css     # стилі
│
└── data/                  # проміжні JSON-файли (у .gitignore)
    ├── authors.json
    └── quotes.json
```
---

## Оригінал завдання

### Домашнє завдання #10

У минулій домашній роботі ви виконували скрапінг сайту http://quotes.toscrape.com.

Вам необхідно самостійно реалізувати аналог такого сайту на Django.

1. Реалізуйте можливість реєстрації на сайті та вхід на сайт.
2. Можливість додавання нового автора на сайт лише для зареєстрованого користувача.
3. Можливість додавання нової цитати на сайт із зазначенням автора тільки для зареєстрованого користувача.
4. Виконайте міграцію бази даних із MongoDB, яка у вас є, у Postgres для вашого сайту. Можна реалізувати кастомним
   скриптом. (За бажанням можете залишити та працювати з цитатами та авторами в MongoDB, а з користувачами у Postgres)
5. Можна зайти на сторінку кожного автора без автентифікації користувача
6. Усі цитати доступні для перегляду без автентифікації користувача

#### Додаткова частина

1. Реалізуйте пошук цитат за тегами. При натисканні на тег, виводиться список цитат з цим тегом.
2. Реалізуйте блок "Top Ten tags" та виведення найпопулярніших тегів.
3. Реалізуйте пагінацію. Це кнопки next та previous
4. Замість перенесення даних з бази даних MongoDB, реалізуйте можливість скрапінгу даних прямо з вашого сайту по натисканню певної кнопки на формі та наповнення бази даних сайту.

---

## Міграція даних

Реалізовано кастомний скрипт migrate_data.py:

- Підключається до MongoDB Atlas (через mongodb+srv://).

- Експортує дані у data/authors.json та data/quotes.json.

- Імпортує дані у PostgreSQL через Django ORM.

- Якщо Atlas недоступний — використовує локальні JSON-файли.

- Якщо немає навіть JSON — виводить повідомлення про помилку.

---

## Docker Compose

У docker-compose.yml є три сервіси:

- postgres — PostgreSQL (основна база для HW10).

- mongo — локальний MongoDB (резервний варіант).

- web — Django‑сайт HW10.

⚠️ Основне джерело даних — MongoDB Atlas, локальний контейнер mongo використовується лише як запасний варіант.

## Запуск та тестування

1. Створіть файл `.env` у корені проєкту на основі `.env.example`:

```env
    # PostgreSQL
POSTGRES_DB=homework10_db
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_pass

# MongoDB Atlas
MONGO_USER=atlas_user
MONGO_PASS=atlas_pass
MONGO_DB=homework9_db
MONGO_DOMAIN=cluster0.xxxxx.mongodb.net

# Django
DJANGO_SECRET_KEY=your_secret_key_here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

```

2. Підніміть середовище:

```bash
    docker compose up -d
```

3. Виконайте міграцію:

```bash
    docker compose exec web python quotes_site/manage.py migrate
```
4. Запустіть базові тести:

```bash
docker compose exec web python quotes_site/manage.py test quotes
```
```text    
    ✅ Очікуваний результат
    Після успішного тестування ви побачите щось на кшталт:
    Found 9 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 2.376s

    OK
    Destroying test database for alias 'default'...

    - Found 9 test(s). — знайдено всі тести.
```
- ........ — кожна крапка означає успішний тест.

- OK — підтвердження, що всі тести пройшли.

- База даних для тестів автоматично створюється й видаляється після перевірки.

- ⚠️ Попередження типу UnorderedObjectListWarning або urls.W005 не є критичними й не впливають
 на роботу сайту.

5. Створіть суперкористувача:

```bash
    docker compose exec web python quotes_site/manage.py createsuperuser
```

6. Перенесіть дані з MongoDB Atlas у Postgres:

```bash
    docker compose exec web python quotes_site/migrate_data.py
```

7. Перевірте роботу сайту згідно фуннкціоналу на http://localhost:8000.


