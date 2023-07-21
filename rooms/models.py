from django.db import models
from hotels.models import Hotel


# Create your models here.


class Type(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.room_number
