from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=200)  # e.g. "Central Government Museum"
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)  # optional: how many seats

    # you can expand later (map coords, etc.)
    # latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    place = models.ForeignKey(Place, on_delete=models.PROTECT, related_name='events')
    # PROTECT = you cannot delete a place if events still reference it

    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    # optional poster in future. For now you can leave blank, even if you don't have media yet.

    is_published = models.BooleanField(default=True)  # visible to public or not

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
            models.Index(fields=['is_published']),
            models.Index(fields=['place']),
        ]