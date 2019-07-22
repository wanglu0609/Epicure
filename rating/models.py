from django.db import models

# Create your models here.
class Restaurant(models.Model):
    res_ID = models.CharField(max_length=200,primary_key=True)
    name = models.CharField(max_length=200,null=True)
    averageRating=models.FloatField(null=True)
    Cuisine_Type = models.CharField(max_length=255,null=True)
    Price_Range = models.CharField(max_length = 200,null=True)
    Phone = models.CharField(max_length = 200,null=True)
    Address = models.CharField(max_length=255,null=True)
    Hours_Start = models.CharField(max_length = 200,null=True)
    Hours_End = models.CharField(max_length = 200,null=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0,null=True)
    dish_type = models.CharField(max_length=200,null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('restaurant', 'name'),)

    def __str__(self):
        return self.name

# class User(models.Model):
#     ID = models.IntegerField(max_length=200,primary_key=True)
#     name = models.CharField(max_length=200,null=True)
#     Password = models.CharField(max_length=255,null=True)
#     Major = models.CharField(max_length = 200,null=True)
#     Gender = models.CharField(max_length = 10,null=True)
#     Favorite_Cuisine_Type = models.CharField(max_length=255,null=True)
#     Favorite_Restaurant_Type = models.CharField(max_length = 200,null=True)

#     def __str__(self):
#         return self.name
