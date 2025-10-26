from django.db import models
from django.utils import timezone
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    # slug = 'news', 'exhibitions', etc.

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='articles')

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)

    summary = models.TextField(blank=True, help_text="Short preview / intro text.")
    body = models.TextField()

    cover_image = models.ImageField(upload_to='article_covers/', blank=True, null=True)

    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['published_at']),
            models.Index(fields=['is_published']),
            models.Index(fields=['category']),
            models.Index(fields=['author']),
        ]