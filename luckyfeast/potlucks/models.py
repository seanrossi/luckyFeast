from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    event_id = models.AutoField
    event_id.primary_key=True
    event_key = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=40, default="")
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=50, default="")
    #address = models.CharField(max_length=30, default="")
    #apt = models.CharField(max_length=6, default="")
    #city = models.CharField(max_length=30, default="")
    #state = models.CharField(max_length=2, default="")
    #zipcode = models.CharField(max_length=5, default="")
    rsvp_count = models.IntegerField(default=0)

class Dish_Type_Main(models.Model):
    main_type = models.CharField(max_length=20, default="")

class Dish_Type_Sub(models.Model):
    main_type = models.ForeignKey(Dish_Type_Main, on_delete=models.CASCADE)
    sub_type = models.CharField(max_length=20, default="")
    def __str__(self):
        return self.main_type.main_type + ":" + self.sub_type

class Event_Dish_Tally(models.Model):
    tally_id = models.AutoField
    tally_id.primary_key=True
    app_needed = models.IntegerField(default=0) 
    app_assigned = models.IntegerField(default=0) 
    soup_needed = models.IntegerField(default=0) 
    soup_assigned = models.IntegerField(default=0) 
    salad_needed = models.IntegerField(default=0) 
    salad_assigned = models.IntegerField(default=0) 
    entree_needed = models.IntegerField(default=0) 
    entree_assigned = models.IntegerField(default=0) 
    dessert_needed = models.IntegerField(default=0) 
    dessert_assigned = models.IntegerField(default=0) 
    beverage_needed = models.IntegerField(default=0) 
    beverage_assigned = models.IntegerField(default=0) 
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Assignment(models.Model):
    dish_id = models.AutoField
    dish_id = primary_key=True
    dish_type = models.CharField(max_length=20, default="")
    dish_name = models.CharField(max_length=20, default="")
    assignment_status = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Guest_Instance(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=30, default="")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    RSVP_UNDECIDED = 1
    RSVP_YES = 2
    RSVP_NO = 3
    RSVP_CHOICES = (
        (RSVP_UNDECIDED, 'Undecided'),
        (RSVP_YES, 'Yes'),
        (RSVP_NO, 'No')
    )
    rsvp_status = models.IntegerField(choices=RSVP_CHOICES, default=RSVP_UNDECIDED)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
       
class Ingredient(models.Model):
    ingredient_id = models.AutoField
    ingredient_id.primary_key=True
    name = models.CharField(max_length=20)
    calories = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
 
# Create your models here.
