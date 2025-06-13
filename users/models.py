from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone # Added import
from .calculators import ACTIVITY_LEVEL_CHOICES

class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, null=True, blank=True, help_text='Select your typical daily activity level.')
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Weight in kilograms')
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Height in centimeters')
    diseases = models.ManyToManyField(Disease, blank=True, related_name='user_conditions')
    # Add any other custom fields for the user here

    def __str__(self):
        return self.username

class UserHealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_data')
    date = models.DateField(default=timezone.now) # Use default instead of auto_now_add for more flexibility
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text='Body Mass Index')
    bmr = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='Basal Metabolic Rate')
    daily_calorie_target = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.date}'
