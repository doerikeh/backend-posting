from django.contrib import admin
from tinymce.models import TinyMCE
from .models import Posting, Categories, Comment
from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


@admin.register(Posting)
class ArtikelAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Artikel", {"fields": ("user", "title", "categories","posting", "images", "is_published")}),
    )

    list_display = ("user", "title", "slug", "date_created", "viewed", "is_published", )
    list_filter = ("date_created",)
    search_fields = ("user", "title", "date_created")
    list_max_show_all = 900
    list_per_page = 30
    readonly_fields=('date_created',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

    def posting_tag(self, obj):
        if obj.images:
            return format_html('<img src="%s" width="200" heigth="200" />' % obj.images.url)
        return "-"
    posting_tag.short_deskription = "images"

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Categories", {"fields": ("title", "image",)}),
    )

    list_display = ("title", "image", "slug", "date_created", )
    list_filter = ("date_created",)

    def categories_tag(self, obj):
        if obj.image:
            return format_html('<img src="%s" width="200" heigth="200" />' % obj.image.url)
        return "-"
    categories_tag.short_deskription = "image"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Comment", {"fields": ("posting", "comment", "email")}),
    )
    list_display = ("email" ,"posting", "comment", "date_created", "image")
    list_filter = ("date_created",)


