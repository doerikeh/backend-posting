from django.db import models
import os
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

def profile_project_to(instance, filename):
    now = timezone_now()
    slug = instance.slug
    base, ext = os.path.splitext(filename)
    return f"image/project/{slug}/{now:%Y%m%d/%H%M%S}{ext.lower()}"

def profile_upload_to(instance, filename):
    now = timezone_now()
    slug = instance.slug
    base, ext = os.path.splitext(filename)
    return f"image/profile/{slug}/{now:%Y%m%d/%H%M%S}{ext.lower()}"

def profile_media_upload_to(instance, filename):
    now = timezone_now()
    slug = instance.slug
    base, ext = os.path.splitext(filename)
    return f"media/profile/{slug}/{now:%Y%m%d/%H%M%S}{ext.lower()}"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError("Harus Menggunakan Email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_field):
        extra_field.setdefault("is_staff", False)
        extra_field.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_field)


    def create_superuser(self, email, password=None, **extra_field):
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser", True)
        if extra_field.get("is_staff") is not True:
            raise ValueError(
            "superuser must have is_staff=True"
        )
        if extra_field.get("is_superuser") is not True:
            raise ValueError(
            "superuser must have is_superuser=True"
        )
        return self._create_user(email, password, **extra_field)

        

class User(AbstractUser):
    username = None
    username_user = models.CharField(max_length=90, blank=False, null=False)
    email = models.EmailField('email address', unique=True, blank=True, null=False)
    image_profile = models.ImageField(upload_to=profile_upload_to)
    image_profile_project = models.ImageField(upload_to=profile_media_upload_to, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def __str__(self):
        return f"{self.username_user}"

    @property
    def is_employee(self):
        return self.is_active and(
            self.is_superuser or self.is_staff and self.groups.filter(name="Employess").exists()
        )
    
    @property
    def is_dispatcher(self):
        return self.is_active and (
            self.is_superuser or self.is_staff and self.groups.filter(name="Dispatchers").exists()
        )
    
    def get_absolute_url(self):
        return reverse("base:user-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username_user)
        super(User, self).save(*args, **kwargs)

class Projects(models.Model):
    CHOICES_PROJECT = (
        ("Done", "Done"),
        ("Pending", "Pending"),
        ("Cancel", "cancel")
    )
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    title  = models.CharField(max_length=255, unique=True, blank=False, null=True)
    slug = models.SlugField()
    image_project = models.ImageField(upload_to=profile_project_to, null=True)
    image_1 = models.ImageField(upload_to=profile_project_to, null=True)
    image_2 = models.ImageField(upload_to=profile_project_to, null=True)
    tentang = models.TextField()
    pengertian = models.CharField(max_length=900,blank=False, null=True)
    kelebihan = models.CharField(max_length=900,blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    tgl_project = models.DateField(auto_now=False)
    progress = models.CharField(max_length=80, choices=CHOICES_PROJECT)


    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Projects, self).save(*args, **kwargs)