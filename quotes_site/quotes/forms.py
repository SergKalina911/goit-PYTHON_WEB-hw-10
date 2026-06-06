""" Forms for the quotes app. This module defines forms for creating and managing authors, quotes,
tags, as well as user registration and login. It also includes a search form for finding authors
by name."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Author, Quote, Tag

class AuthorForm(forms.ModelForm):
    """ Форма для створення та редагування авторів """
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]

class QuoteForm(forms.ModelForm):
    """ Форма для створення та редагування цитат """
    class Meta:
        model = Quote
        fields = ["quote", "author", "tags"]

class TagForm(forms.ModelForm):
    """ Форма для створення та редагування тегів """
    class Meta:
        model = Tag
        fields = ["name"]

class RegisterForm(UserCreationForm):
    """ Форма для реєстрації нового користувача з email """
    email = forms.EmailField(required=True, help_text="Вкажіть вашу електронну пошту")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        """ Зберігає користувача з email у базі """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    """ Форма для входу користувача """
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class AuthorSearchForm(forms.Form):
    """ Форма для пошуку автора за ім'ям. Використовується на сторінці списку авторів для
    фільтрації результатів. """
    fullname = forms.CharField(label="Ім'я автора", max_length=200)
