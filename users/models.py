from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Role(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return str(self.user.username)