from django.db import models


# Create your models here.

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=255)
    star_rating = models.FloatField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.hotel_name
