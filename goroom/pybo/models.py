from django.contrib.auth.models import User
from django.db import models

from django.db import models

class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

class Building(models.Model):
    building_type = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.CharField(max_length=255)

    label1 = models.CharField(max_length=50, default="월세")
    price1 = models.IntegerField(blank=True, null=True)

    label2 = models.CharField(max_length=50, default="전세")
    price2 = models.IntegerField(blank=True, null=True)

    label3 = models.CharField(max_length=50, default="매매")
    price3 = models.IntegerField(blank=True, null=True)

class BuildingImage(models.Model):
    building = models.ForeignKey(Building, related_name='images', on_delete=models.CASCADE)
    image = models.CharField(max_length=255)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)