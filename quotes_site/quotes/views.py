""" Огляд основних представлень для додатку цитат. """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import requests
from bs4 import BeautifulSoup
from django.db.models import Count
from .models import Author, Quote, Tag
from .forms import AuthorForm, QuoteForm, TagForm, AuthorSearchForm, RegisterForm

def index(request):
    """ Головна сторінка сайту, яка відображає останні цитати та популярні теги. """
    quotes = Quote.objects.all().order_by("-created_at")[:10]
    top_tags = Tag.objects.annotate(num_quotes=Count("quote")).order_by("-num_quotes")[:10]
    return render(request, "quotes/index.html", {"quotes": quotes, "top_tags": top_tags})

def quote_list(request):
    """ Сторінка зі списком усіх цитат з пагінацією. """
    quotes = Quote.objects.all().order_by("id")
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "quotes/quote_list.html", {"page_obj": page_obj})

def quote_detail(request, pk):
    """ Сторінка деталей цитати. """
    quote = get_object_or_404(Quote, pk=pk)
    return render(request, "quotes/quote_detail.html", {"quote": quote})

def author_detail(request, pk):
    """ Сторінка деталей автора. """
    author = get_object_or_404(Author, pk=pk)
    quotes = Quote.objects.filter(author=author)
    return render(request, "quotes/author_detail.html", {"author": author, "quotes": quotes})

def register(request):
    """ Сторінка реєстрації нового користувача з email. """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація успішна! Ви увійшли у систему.")
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "quotes/register.html", {"form": form})

def user_login(request):
    """ Сторінка входу користувача. """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вхід виконано успішно.")
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "quotes/login.html", {"form": form})

def user_logout(request):
    """ Вихід користувача. """
    logout(request)
    messages.info(request, "Ви вийшли із системи.")
    return redirect("index")

@login_required
def add_author(request):
    """ Додавання нового автора. """
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Автора додано успішно.")
            return redirect("index")
    else:
        form = AuthorForm()
    return render(request, "quotes/add_author.html", {"form": form})

@login_required
def add_quote(request):
    """ Додавання нової цитати. """
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Цитату додано успішно.")
            return redirect("quote_list")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})

@login_required
def add_tag(request):
    """ Додавання нового тегу. """
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Тег додано успішно.")
            return redirect("index")
    else:
        form = TagForm()
    return render(request, "quotes/add_tag.html", {"form": form})

def search_by_tag(request, tag_name):
    """ Пошук цитат за тегом. """
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.filter(tags=tag)
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "quotes/quote_list.html", {"page_obj": page_obj, "tag": tag})

def search_by_author(request):
    """ Пошук цитат за автором. """
    quotes = []
    if request.method == "POST":
        form = AuthorSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["fullname"]
            author = Author.objects.filter(fullname__icontains=name).first()
            if author:
                quotes = Quote.objects.filter(author=author)
    else:
        form = AuthorSearchForm()
    return render(request, "quotes/search_author.html", {"form": form, "quotes": quotes})

@login_required
def scrape_quotes(request):
    """ Скрапінг цитат з http://quotes.toscrape.com. """
    url = "http://quotes.toscrape.com/page/1/"
    count = 0
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for quote_block in soup.select(".quote"):
            text = quote_block.select_one(".text").get_text(strip=True)
            author_name = quote_block.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in quote_block.select(".tag")]

            author_link = quote_block.select_one("span a")["href"]
            author_url = "http://quotes.toscrape.com" + author_link
            author_page = requests.get(author_url)
            author_soup = BeautifulSoup(author_page.text, "html.parser")

            born_date = author_soup.select_one(".author-born-date").get_text(strip=True)
            born_location = author_soup.select_one(".author-born-location").get_text(strip=True)
            description = author_soup.select_one(".author-description").get_text(strip=True)

            author, _ = Author.objects.get_or_create(fullname=author_name)
            author.born_date = born_date
            author.born_location = born_location
            author.description = description
            author.save()

            quote, created = Quote.objects.get_or_create(quote=text, author=author)
            if created:
                count += 1

            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)

        next_btn = soup.select_one(".next > a")
        url = "http://quotes.toscrape.com" + next_btn["href"] if next_btn else None

    messages.success(request, f"Скрапінг завершено! Додано {count} нових цитат.")
    return redirect("index")

@login_required
def clear_database(request):
    """ Очищення бази даних від авторів, цитат та тегів. """
    Quote.objects.all().delete()
    Author.objects.all().delete()
    Tag.objects.all().delete()
    messages.success(request, "Базу очищено успішно.")
    return redirect("index")
