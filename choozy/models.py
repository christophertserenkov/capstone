from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class User(AbstractUser):
    pass

class Player(models.Model):
    username = models.CharField(max_length=32)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'

class Room(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')
    players = models.ManyToManyField(Player, related_name='room')
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    city = models.CharField(max_length=64)
    country_code = models.CharField(max_length=2)

    def __str__(self):
        return f"Table {self.id} by {self.creator}"
    

class Submission(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='responses')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='responses')
    categories = models.TextField()
    price = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    parking = models.BooleanField(default=False)
    outdoor = models.BooleanField(default=False)


class Result(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='results')
    restraunt_name = models.CharField(max_length=128)
    image_url = models.TextField()
    menu_url = models.TextField(null=True, blank=True)
    yelp_url = models.TextField()
    phone = models.CharField(max_length=16)
    display_phone = models.CharField(max_length=32)
    rating = models.FloatField()
    price = models.CharField(max_length=4)
    categories = models.TextField()

