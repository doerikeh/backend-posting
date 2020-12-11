from django.db import models
from profiles.models import User
from django.template.defaultfilters import slugify
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
import os

def posting_to(instance, filename):
    now = timezone_now()
    slug = instance.slug
    base, ext = os.path.splitext(filename)
    return f"image/posting/{slug}/{now:%Y%m%d/%H%M%S}{ext.lower()}"

def categories_to(instance, filename):
    now = timezone_now()
    slug = instance.slug
    base, ext = os.path.splitext(filename)
    return f"image/categories/{slug}/{now:%Y%m%d/%H%M%S}{ext.lower()}"

def comment_to(instance, filename):
    now = timezone_now()
    base, ext = os.path.splitext(filename)
    return f"image/comment/{now:%Y%m%d/%H%M%S}{ext.lower()}"


class Categories(models.Model):
    title= models.CharField(max_length=80, null=False)
    image = models.ImageField(upload_to=categories_to)
    slug  = models.SlugField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Categories, self).save(*args, **kwargs)

class Posting(models.Model):
    title = models.CharField(max_length=255)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="posting_categories")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed = models.IntegerField(default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to=posting_to, max_length=500)
    slug = models.SlugField()
    posting = models.TextField()
    is_published = models.BooleanField(default=False)

    class Meta:
       ordering = ('-date_created',)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Posting, self).save(*args, **kwargs)

class Comment(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name="post_comments")
    image = models.ImageField(default="image/user.png", upload_to=comment_to)
    date_created = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField()
    email   = models.EmailField(null=False)

    def __str__(self):
        return f"{self.posting.title} - {self.email}"

    class Meta:
       ordering = ('-date_created',)