""" Огляд основних представлень для додатку цитат. """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import requests
from bs4 import BeautifulSoup

from .models import Author, Quote, Tag
from .forms import AuthorForm, QuoteForm, TagForm, AuthorSearchForm

def index(request):
    """ Головна сторінка сайту, яка відображає останні цитати та популярні теги. Використовує
    пагінацію для відображення цитат та надає користувачам можливість швидко переглянути найновіші
    цитати та популярні теми.  Показує останні 10 цитат та 10 популярних тегів. """
    quotes = Quote.objects.order_by("-id")[:10]
    top_tags = Tag.objects.all()[:10]
    return render(request, "quotes/index.html", {"quotes": quotes, "top_tags": top_tags})

def quote_list(request):
    """ Сторінка зі списком усіх цитат. Використовує пагінацію для зручного перегляду великої
    кількості цитат. Користувачі можуть переглядати цитати по 10 на сторінці та переходити між
    сторінками для перегляду інших цитат. """
    quotes = Quote.objects.all().order_by("id")
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "quotes/quote_list.html", {"page_obj": page_obj})

def quote_detail(request, pk):
    """ Сторінка деталей цитати. Відображає повний текст цитати та інформацію про автора. """
    quote = get_object_or_404(Quote, pk=pk)
    return render(request, "quotes/quote_detail.html", {"quote": quote})

def author_detail(request, pk):
    """ Сторінка деталей автора. Відображає інформацію про автора та список його цитат. """
    author = get_object_or_404(Author, pk=pk)
    quotes = Quote.objects.filter(author=author)
    return render(request, "quotes/author_detail.html", {"author": author, "quotes": quotes})

def register(request):
    """ Сторінка реєстрації нового користувача. Використовує стандартну форму реєстрації Django для
    створення нового облікового запису.  """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "quotes/register.html", {"form": form})

def user_login(request):
    """ Сторінка входу користувача. Використовує стандартну форму аутентифікації Django для
    аутентифікації користувача. """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "quotes/login.html", {"form": form})

def user_logout(request):
    """ Функція для виходу користувача. Використовує стандартну функцію logout Django для завершення
    сеансу користувача. Після виходу користувач буде перенаправлений на головну сторінку. """
    logout(request)
    return redirect("index")

@login_required
def add_author(request):
    """ Сторінка для додавання нового автора. Використовує форму AuthorForm для збору інформації
    про автора та збереження її в базі даних. Доступна лише для авторизованих користувачів. Після
    успішного додавання автора користувач буде перенаправлений на головну сторінку. """
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = AuthorForm()
    return render(request, "quotes/add_author.html", {"form": form})

@login_required
def add_quote(request):
    """ Сторінка для додавання нової цитати. Використовує форму QuoteForm для збору інформації
    про цитату та збереження її в базі даних. Доступна лише для авторизованих користувачів. Після
    успішного додавання цитати користувач буде перенаправлений на сторінку зі списком цитат. """
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quote_list")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})

@login_required
def add_tag(request):
    """ Сторінка для додавання нового тегу. Використовує форму TagForm для збору інформації
    про тег та збереження її в базі даних. Доступна лише для авторизованих користувачів. Після
    успішного додавання тегу користувач буде перенаправлений на головну сторінку. """
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = TagForm()
    return render(request, "quotes/add_tag.html", {"form": form})

def search_by_tag(request, tag_name):
    """ Сторінка для пошуку цитат за тегом. Відображає всі цитати, які мають вказаний тег.
    Використовує пагінацію для зручного перегляду результатів. Користувачі можуть переглядати
    цитати по 10 на сторінці та переходити між сторінками для перегляду інших цитат з відповідним
    тегом. """
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.filter(tags=tag)
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "quotes/quote_list.html", {"page_obj": page_obj, "tag": tag})

def search_by_author(request):
    """ Сторінка для пошуку цитат за автором. Дозволяє користувачам ввести ім'я автора та
    відображає всі цитати, які належать цьому автору. Використовує форму AuthorSearchForm для збору
    інформації про автора та відображає результати на тій же сторінці. Якщо автор не знайдений,
    користувач побачить порожній список цитат. Користувачі можуть переглядати цитати по 10 на сторінці
    та переходити між  сторінками для перегляду інших цитат цього автора. """
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
    """ Функція для скрапінгу цитат з сайту http://quotes.toscrape.com. Використовує бібліотеки
    requests та BeautifulSoup для отримання та парсингу HTML сторінок. Збирає текст цитат, ім'я
    автора та теги, а також додаткову інформацію про автора (дату народження, місце народження та
    опис) зі сторінки автора. Зберігає отримані дані в базі даних, створюючи нові записи для
    авторів, цитат та тегів. Доступна лише для авторизованих користувачів."""
    url = "http://quotes.toscrape.com/page/1/"
    count = 0
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for quote_block in soup.select(".quote"):
            text = quote_block.select_one(".text").get_text(strip=True)
            author_name = quote_block.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in quote_block.select(".tag")]

            # посилання на сторінку автора
            author_link = quote_block.select_one("span a")["href"]
            author_url = "http://quotes.toscrape.com" + author_link
            author_page = requests.get(author_url)
            author_soup = BeautifulSoup(author_page.text, "html.parser")

            born_date = author_soup.select_one(".author-born-date").get_text(strip=True)
            born_location = author_soup.select_one(".author-born-location").get_text(strip=True)
            description = author_soup.select_one(".author-description").get_text(strip=True)

            # створюємо/оновлюємо автора
            author, _ = Author.objects.get_or_create(fullname=author_name)
            author.born_date = born_date
            author.born_location = born_location
            author.description = description
            author.save()

            # створюємо цитату
            quote, created = Quote.objects.get_or_create(quote=text, author=author)
            if created:
                count += 1

            # додаємо теги
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)

        # наступна сторінка
        next_btn = soup.select_one(".next > a")
        url = "http://quotes.toscrape.com" + next_btn["href"] if next_btn else None

    messages.success(request, f"Скрапінг завершено! Додано {count} нових цитат.")
    return redirect("index")

@login_required
def clear_database(request):
    """ Функція для очищення бази даних від усіх авторів, цитат та тегів. Використовується для
    швидкого видалення всіх даних та початку з чистого аркуша. Доступна лише для авторизованих
    користувачів. Після очищення бази даних користувач буде перенаправлений на головну сторінку
    з повідомленням про успішне очищення. """
    Quote.objects.all().delete()
    Author.objects.all().delete()
    Tag.objects.all().delete()
    messages.success(request, "Базу очищено успішно.")
    return redirect("index")
