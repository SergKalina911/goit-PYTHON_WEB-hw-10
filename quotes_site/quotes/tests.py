""" Tests for the quotes app. This module includes unit tests for the Author, Quote, and Tag
models, as well as tests for the main views of the application. The tests cover model creation,
string representations, and the functionality of the index, author detail, quote detail, and search
by tag views. Additionally, there are tests for user registration and login to ensure that
authentication works correctly. These tests help ensure the integrity of the application's core
features and provide a safety net for future code changes.  """
# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import Author, Quote, Tag
from django.contrib.auth.models import User

class AuthorModelTest(TestCase):
    """ Тестування моделі Author. Перевіряє створення автора та його строкове представлення. """
    def test_create_author(self):
        """ Тестує створення автора та перевіряє, що його строкове представлення повертає повне
        ім'я. """
        author = Author.objects.create(fullname="Test Author", description="Bio")
        self.assertEqual(str(author), "Test Author")
        self.assertEqual(author.fullname, "Test Author")

class TagModelTest(TestCase):
    """ Тестування моделі Tag. Перевіряє створення тега та його строкове представлення. """
    def test_create_tag(self):
        """ Тестує створення тега та перевіряє, що його строкове представлення повертає назву тега. """
        tag = Tag.objects.create(name="wisdom")
        self.assertEqual(str(tag), "wisdom")

class QuoteModelTest(TestCase):
    """ Тестування моделі Quote. Перевіряє створення цитати та її строкове представлення. """
    def setUp(self):
        self.author = Author.objects.create(fullname="Author One")
        self.tag = Tag.objects.create(name="life")

    def test_create_quote(self):
        """ Тестує створення цитати та перевіряє, що його строкове представлення повертає текст
        цитати. """
        quote = Quote.objects.create(quote="Life is beautiful", author=self.author)
        quote.tags.add(self.tag)
        self.assertEqual(str(quote), "Life is beautiful")
        self.assertIn(self.tag, quote.tags.all())

class ViewsTest(TestCase):
    """ Тестування основних представлень додатку. Перевіряє, що сторінки завантажуються успішно
    та містять очікуваний контент. """
    def setUp(self):
        """ Налаштовує тестовий клієнт та створює тестового автора і цитату для використання в
        тестах. """
        self.client = Client()
        self.author = Author.objects.create(fullname="Author Two")
        self.quote = Quote.objects.create(quote="Test Quote", author=self.author)

    def test_index_view(self):
        """ Тестує, що головна сторінка завантажується успішно та містить привітальне
        повідомлення. """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ласкаво просимо")

    def test_author_detail_view(self):
        """ Тестує, що сторінка деталей автора завантажується успішно та містить ім'я автора. """
        response = self.client.get(reverse("author_detail", args=[self.author.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.fullname)

    def test_quote_detail_view(self):
        """ Тестує, що сторінка деталей цитати завантажується успішно та містить текст цитати. """
        response = self.client.get(reverse("quote_detail", args=[self.quote.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.quote.quote)

    def test_search_by_tag_view(self):
        """ Тестує, що сторінка пошуку за тегом завантажується успішно та містить цитати з
        відповідним тегом. """
        tag = Tag.objects.create(name="testtag")
        self.quote.tags.add(tag)
        response = self.client.get(reverse("search_by_tag", args=[tag.name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.quote.quote)

class AuthTest(TestCase):
    """ Тестування функціональності автентифікації. Перевіряє реєстрацію та вхід користувача. """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_register_view(self):
        """ Тестує, що сторінка реєстрації завантажується успішно та дозволяє створити нового
        користувача. """
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        })
        self.assertEqual(response.status_code, 302)  # redirect after success

    def test_login_view(self):
        """ Тестує, що сторінка входу завантажується успішно та дозволяє увійти з правильними
        обліковими даними. """
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass"
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
