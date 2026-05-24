
""" Models for the quotes app. This module defines the Author, Quote, and Tag models, which are
used to store information about authors, their quotes, and associated tags. The Author model
includes fields for the author's full name, birth date, birth location, and a description. The
Quote model includes the quote text, a foreign key to the Author, and a many-to-many relationship
with the Tag model. The Tag model includes a unique name field for categorizing quotes. Each model
also has a __str__ method to provide a human-readable representation of the objects, which is
especially useful in the Django admin interface and other parts of the site where these models
are displayed. """
from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Author(models.Model):
    """ Модель для зберігання інформації про авторів цитат. Включає поля для повного імені, дати
    народження, місця народження та опису. Поле fullname є унікальним, щоб уникнути дублювання
    авторів. """
    fullname = models.CharField(max_length=200, unique=True)
    born_date = models.CharField(max_length=100, blank=True)
    born_location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        """ Повертає повне ім'я автора при виводі об'єкта Author. Це полегшує ідентифікацію авторів
        у адмінці та інших частинах сайту. """
        return self.fullname

class Tag(models.Model):
    """ Модель для зберігання тегів. Поле name є унікальним, щоб уникнути дублювання тегів. """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """ Повертає назву тега при виводі об'єкта Tag. Це полегшує ідентифікацію тегів у
        адмінці та інших частинах сайту. """
        return self.name

class Quote(models.Model):
    """ Модель для зберігання цитат. """
    quote = models.TextField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)  # нове поле

    def __str__(self):
        """ Повертає перші 50 символів цитати при виводі об'єкта Quote. Це полегшує ідентифікацію
        цитат у адмінці та інших частинах сайту. """
        return self.quote[:50]
