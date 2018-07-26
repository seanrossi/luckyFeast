# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from potlucks.models import Dish_Type_Main, Dish_Type_Sub

class Time_Figure(models.Model):
    prep_time = models.IntegerField(default=0)
    cook_time = models.IntegerField(default=0)
    cool_time = models.IntegerField(default=0)
    def __str__(self):
        return self.prep_time + self.cook_time + self.cool_time

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dish_type = models.ForeignKey(Dish_Type_Sub, on_delete=models.SET_NULL, null=True)
    serving_size = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_time = Time_Figure

class Ingredient_Instance(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.IntegerField(default=0)

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    order_number = models.IntegerField(default=0)
    text = models.TextField(max_length="400")

# Create your models here.
