from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models



# Create your models here.
class WatchList(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_title = models.CharField(max_length=255)
    movie_id = models.CharField(max_length=15)
    added_at = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-added_at']
        unique_together = ['user', 'movie_id']


class SeenList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_title = models.CharField(max_length=255)
    movie_id = models.CharField(max_length=15)
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True
    )


    class Meta:
        ordering = ['-added_at']
        unique_together = ['user', 'movie_id']
