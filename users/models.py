from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .choices.role_choices import TEXT_CHOICES
from rooms.models import Room


# Create your models here.


class Role(models.Model):
    role_name = models.CharField(max_length=50, choices=TEXT_CHOICES)

    def __str__(self):
        return self.role_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return str(self.user.username)


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500)

    def __str__(self):
        return self.token


class InvalidToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token


class Booking(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False)


class BookingDetail(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.FloatField()
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
