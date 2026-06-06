# goit-PYTHON_WEB-hw-10

# HW10, HW13 – Django + PostgreSQL + MongoDB (міграція даних)

## Опис

У HW09 дані (автори та цитати) зберігалися у MongoDB.  
У HW10 сайт працює на PostgreSQL, тому потрібно перенести дані.
У HW13 додано скидання паролю користувача через пошту. Усі змінні середовища зберігаються у файлі .env та використовуватися у файлі settings.py

---

## 🚀 Функціонал
- Реєстрація та логін користувачів — через власну форму з email, підтримка скидання паролю.
- Додавання авторів і цитат — доступно лише для автентифікованих користувачів.
- Перегляд авторів та цитат — доступний без входу.
- Пошук цитат за тегами — сторінка з пагінацією.
- Пошук цитат за автором — через форму пошуку.
- Пагінація — кнопки «Попередня» / «Наступна» для зручного перегляду.
- Блок “Top Ten Tags” — відображає найпопулярніші теги.
- Скрапінг цитат із сайту quotes.toscrape.com — автоматичне завантаження авторів, цитат і тегів.
- Очищення бази — кнопка на головній сторінці для видалення всіх даних.
- Міграція даних з MongoDB Atlas у PostgreSQL — через скрипт migrate_data.py.

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
│       │   ├── base.html                       # базовий шаблон з меню та стилями
│       │   ├── index.html                      # головна сторінка з останніми цитатами
│       │   ├── author_detail.html              # сторінка автора з його цитатами
│       │   ├── quote_detail.html               # деталі цитати
│       │   ├── quote_list.html                 # список цитат (з пагінацією)
│       │   ├── add_author.html                 # форма додавання автора
│       │   ├── add_quote.html                  # форма додавання цитати
│       │   ├── add_tag.html                    # форма додавання тега
│       │   ├── search_author.html              # пошук цитат за автором
│       │   ├── register.html                   # шаблон для реєстрації користувача
│       │   ├── login.html                      # шаблон для входу
│       │   ├── password_reset.html             # форма для запиту скидання паролю
│       │   ├── password_reset_done.html        # повідомлення після запиту
│       │   ├── password_reset_confirm.html     # форма для введення нового паролю
│       │   ├── password_reset_complete.html    # повідомлення після успішної зміни
│       │   ├── password_reset_email.html       # текст листа з посиланням
│       │   └── password_reset_subject.txt      # тема листа
│       │
│       └── static/quotes/css/style.css         # стилі для сайту
│
└── data/                  # проміжні JSON-файли (у .gitignore)
    ├── authors.json
    └── quotes.json

```
---
## 🔑 Налаштування .env

У репозиторії є файл `.env.example`.  
Він показує, які змінні середовища потрібні для роботи проєкту, але містить лише **шаблонні значення**.

### Що треба зробити:
1. Скопіювати `.env.example` → створити власний файл `.env` у корені проєкту.
2. Замінити значення `POSTGRES_PASSWORD` на свій реальний пароль.
3. Переконатися, що `POSTGRES_HOST=db` (це ім’я сервісу з `docker-compose.yml`).
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

### Домашнє завдання №13(Друга частина)

У цьому домашньому завданні необхідно доопрацювати застосунок Django із домашнього завдання 10.

#### Завдання

- Реалізуйте механізм скидання паролю для зареєстрованого користувача;
- Усі змінні середовища повинні зберігатися у файлі .env та використовуватися у файлі settings.py
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
POSTGRES_DB=yourdbname
POSTGRES_USER=yourusername
POSTGRES_PASSWORD=yourpassword
POSTGRES_PORT=5432
POSTGRES_HOST=postgres
# MongoDB Atlas
MONGO_USER=yourusername
MONGO_PASS=yourpassword
MONGO_DB=yourdbname
MONGO_DOMAIN=yourcluster.mongodb.net

# Django
DJANGO_SECRET_KEY=yoursupersecretkey123
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Email settings
EMAIL_HOST=smtp.meta.ua
EMAIL_PORT=465
EMAIL_HOST_USER=youremail@meta.ua
EMAIL_HOST_PASSWORD=yourpassword
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_USE_SSL=True
DEFAULT_FROM_EMAIL=youremeil@meta.ua

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


