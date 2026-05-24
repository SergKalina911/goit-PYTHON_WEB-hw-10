""" quotes/urls.py - URL конфігурація для додатку quotes. Визначає маршрути для різних сторінок
та функцій додатку, включаючи головну сторінку, список цитат, деталі цитати та автора, пошук за
тегом, а також маршрути для додавання авторів, цитат, тегів, скрапінгу,очищення бази даних,
реєстрації та входу користувачів. Ці маршрути зв'язують URL-адреси з відповідними представленнями
(views) для обробки запитів та відображення відповідного контенту користувачам. """

from django.contrib import admin
from django.urls import path
from quotes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("quotes/", views.quote_list, name="quote_list"),
    path("quote/<int:pk>/", views.quote_detail, name="quote_detail"),
    path("tag/<str:tag_name>/", views.search_by_tag, name="search_by_tag"),
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("add_tag/", views.add_tag, name="add_tag"),
    path("scrape/", views.scrape_quotes, name="scrape_quotes"),
    path("clear/", views.clear_database, name="clear_database"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("search_author/", views.search_by_author, name="search_author"),
    path("author/<int:pk>/", views.author_detail, name="author_detail"),
]
