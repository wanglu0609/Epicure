from django.db import models
from django.contrib.auth.models import User
from rating.models import Restaurant, Dish

# Create your models here.

class Information(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    FirstName = models.CharField(max_length=200,null=True)
    Major = models.CharField(max_length=200,null=True)
    Gender = models.CharField(max_length=200,null=True)
    Favorite_Cuision = models.CharField(max_length=200,null=True)
    Favorite_Restaurant = models.CharField(max_length=200,null=True)
    Rating = models.IntegerField(default=1,null=True)
    Duration = models.IntegerField(default=1,null=True)
    Visit = models.IntegerField(default=1,null=True)
    Price = models.IntegerField(default=1,null=True)

    def __str__(self):
        return self.user.username

class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False,null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendship_creator")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")

    def __str__(self):
        return self.creator

class Reviews(models.Model):
    comment = models.CharField(max_length=250)
    rating = models.IntegerField(default=0,null=True)
    name = models.ForeignKey(Dish, on_delete=models.CASCADE)
    rate_on = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rate_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment