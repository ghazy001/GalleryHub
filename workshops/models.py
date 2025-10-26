from django.db import models
from django.utils import timezone
from events.models import Place  # we already created Place for Events, we can reuse it

class Material(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)  # how many you have in storage
    unit = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. pieces, kg, sets, rolls..."
    )

    def __str__(self):
        return self.name


class Workshop(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200, blank=True)  # person running it
    description = models.TextField(blank=True)

    place = models.ForeignKey(
        Place,
        on_delete=models.PROTECT,
        related_name='workshops'
    )

    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    capacity = models.PositiveIntegerField(default=20)  # max seats
    is_active = models.BooleanField(default=True)  # public or hidden (like draft / canceled)

    materials = models.ManyToManyField(
        Material,
        related_name='workshops',
        blank=True,
        help_text="Materials required for this workshop"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time']),
            models.Index(fields=['is_active']),
            models.Index(fields=['place']),
            models.Index(fields=['capacity']),
        ]