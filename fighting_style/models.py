from django.db import models


class fighting_style(models.Model):
    difficulty_choices = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=20, choices=difficulty_choices)
    required_skills = models.TextField()

    def __str__(self):
        return self.name
