""" quotes/urls.py - URL конфігурація для додатку quotes.
Визначає маршрути для різних сторінок та функцій додатку:
- головна сторінка
- список цитат
- деталі цитати та автора
- пошук за тегом та автором
- додавання авторів, цитат, тегів
- скрапінг та очищення бази
- реєстрація, вхід/вихід користувачів
- механізм скидання паролю
"""

from django.contrib import admin
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from quotes import views

urlpatterns = [
    # Адмінка
    path("admin/", admin.site.urls),

    # Основні сторінки
    path("", views.index, name="index"),
    path("quotes/", views.quote_list, name="quote_list"),
    path("quote/<int:pk>/", views.quote_detail, name="quote_detail"),
    path("author/<int:pk>/", views.author_detail, name="author_detail"),

    # Пошук
    path("tag/<str:tag_name>/", views.search_by_tag, name="search_by_tag"),
    path("search_author/", views.search_by_author, name="search_author"),

    # Додавання
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("add_tag/", views.add_tag, name="add_tag"),

    # Скрапінг та очищення
    path("scrape/", views.scrape_quotes, name="scrape_quotes"),
    path("clear/", views.clear_database, name="clear_database"),

    # Авторизація
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # Скидання паролю (всі шаблони у quotes/templates/quotes)
    path("reset-password/", PasswordResetView.as_view(
        template_name="quotes/password_reset.html",
        email_template_name="quotes/password_reset_email.html",
        subject_template_name="quotes/password_reset_subject.txt",
        success_url=reverse_lazy("password_reset_done")
    ), name="password_reset"),

    path("reset-password/done/", PasswordResetDoneView.as_view(
        template_name="quotes/password_reset_done.html"
    ), name="password_reset_done"),

    path("reset-password/confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
        template_name="quotes/password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete")
    ), name="password_reset_confirm"),

    path("reset-password/complete/", PasswordResetCompleteView.as_view(
        template_name="quotes/password_reset_complete.html"
    ), name="password_reset_complete"),
]
