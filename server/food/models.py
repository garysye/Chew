from django.db import models

class User(models.Model):
  name = models.CharField(max_length=30)

class Cuisine(models.Model):
  name = models.CharField(max_length=255)

class Restaurant(models.Model):
  name = models.CharField(max_length=255)
  location = models.CharField(max_length=255)
  cuisine = models.ForeignKey(Cuisine) # id only

class Food(models.Model):
  name = models.CharField(max_length=255)
  cuisine = models.ForeignKey(Cuisine) # id only
  restaurant = models.ForeignKey(Restaurant)
  price = models.IntegerField()
  avgRating = models.IntegerField()
  numRating = models.IntegerField()

class Review(models.Model):
  text = models.CharField(max_length=255)
  user = models.ForeignKey(User) # id only
  foodRating = models.IntegerField()
  reviewRating = models.IntegerField()
  food = models.ForeignKey(Food) # id only 

class Image(models.Model):
  food = models.ForeignKey(Food) # id only
  image = models.CharField(max_length=255)
  review = models.ForeignKey(Review)

class Tag(models.Model):
  name = models.CharField(max_length=255)

class FoodTag(models.Model):
  food = models.ForeignKey(Food) # id only
  tag = models.ForeignKey(Tag) # id only

