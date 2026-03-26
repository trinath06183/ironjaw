from django.db import models
from django.contrib.auth.models import User
from fighting_style.models import fighting_style  


class fighter_profile(models.Model):
    level_choices = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    selected_fighting_style = models.ForeignKey(fighting_style, on_delete=models.SET_NULL, null=True, blank=True)
    learning_level = models.CharField(max_length=20, choices=level_choices, default='Beginner')

    def __str__(self):
        return self.user.username