from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AdminUser
from django.utils.html import format_html
from .models import User, Projects
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _


@admin.register(User)
class UserAdmin(AdminUser):
    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        ("Personal Info", {"fields": ("username_user", "image_profile", "image_profile_project", "bio",)},),
        ("Permissions",{"fields": ("is_active","is_staff","is_superuser","groups","user_permissions",)},),
        ("Important Date", {"fields": ("last_login", "date_joined")},),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password", "password2",),},),
    )
    list_display = (
        "email",
        "username_user",
        "slug",
        "bio",
        "profile_tag",
        "last_login",
        "date_joined",
        "is_active",
        "is_staff",
    )
    search_fields = ("email", "username_user", "biografi")
    ordering = ("email",)
    list_max_show_all = 900
    list_per_page = 30
    list_filter = ("date_joined", "is_staff", "is_superuser",)

    def profile_tag(self, obj):
        if obj.image_profile:
            return format_html('<img src="%s" width="200" heigth="200" />' % obj.image_profile.url)
        return "-"
    profile_tag.short_deskription = "image_profile"



@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Project", {"fields":("users", "title", "image_project", "image_1","image_2","tentang", "pengertian", "kelebihan","tgl_project", "progress",)},),
    )
    list_display = ("title", "tentang", "tgl_project", "progress", "project_tag",)
    list_filter = ("tgl_project", "progress",)
    search_fields = ("title", )
    list_editable = ("progress",)

    def project_tag(self, obj):
        if obj.image_project:
            return format_html('<img src="%s" width="200" heigth="200" />' % obj.image_project.url)
        return "-"
    project_tag.short_deskription = "image_project"