from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    res_ID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200,null=True)
    score=models.FloatField(null=True,blank=True)
    number_of_visit = models.IntegerField(null=True)
    Cuisine_Type = models.CharField(max_length=255,null=True)
    Price_Range = models.IntegerField(null=True)
    Phone = models.CharField(max_length = 200,null=True)
    Address = models.CharField(max_length=255,null=True)
    Hours_Start = models.IntegerField(null=True)
    Hours_End = models.IntegerField(null=True)
    visit_by = models.ManyToManyField(User, symmetrical=True, blank=True)
    image = models.ImageField(upload_to='image',default ="/image/default.jpg",null=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    dish_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0,null=True)
    dish_type = models.CharField(max_length=200,null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    averageRating=models.FloatField(null=True)
    # class Meta:
    #     unique_together = (('restaurant', 'name'),)

    def __str__(self):
        return self.name

