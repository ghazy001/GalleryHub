from django.db import models
from django.conf import settings
from django.utils import timezone

class Artwork(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, blank=True)  # optional
    description = models.TextField(blank=True)
    year = models.CharField(max_length=50, blank=True)  # flexible (e.g. "1889", "c. 5th century BC")

    image = models.ImageField(upload_to='artworks/', blank=True, null=True)

    is_visible = models.BooleanField(default=True)  # public or hidden
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def thumbnail_url(self):
        # convenience for templates:
        if self.image:
            return self.image.url
        return None  # template will fallback to static placeholder

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['is_visible']),
            models.Index(fields=['artist']),
            models.Index(fields=['year']),
        ]


class ArtworkFeedback(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='feedbacks')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='artwork_feedbacks'
    )

    name = models.CharField(max_length=120, blank=True)
    # if not logged in, we can record a provided name (or "Anonymous")

    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=5,
        help_text="1-5 stars"
    )

    is_approved = models.BooleanField(default=False)  # admin moderation toggle
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback on {self.artwork.title}"
