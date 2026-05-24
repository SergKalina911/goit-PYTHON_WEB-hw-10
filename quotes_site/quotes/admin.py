""" Admin configuration for the quotes app. This module registers the Author, Quote, and Tag
models with the Django admin site, allowing administrators to manage these entities through
the admin interface."""
from django.contrib import admin
from .models import Author, Quote, Tag

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin class for managing authors."""
    list_display = ("fullname", "born_date", "born_location")
    search_fields = ("fullname", "born_location")

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """Admin class for managing quotes."""
    list_display = ("quote", "author")
    search_fields = ("quote",)
    list_filter = ("author", "tags")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin class for managing tags."""
    list_display = ("name",)
    search_fields = ("name",)
