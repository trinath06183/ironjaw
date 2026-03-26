from django.db import models
from django.contrib.auth.models import User
from fighting_style.models import fighting_style


class performance_test(models.Model):
    feedback_choices = (
        ('Correct', 'Correct'),
        ('Incorrect', 'Incorrect'),
        ('Need_Improvement', 'Need Improvement'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fight_style = models.ForeignKey(fighting_style, on_delete=models.SET_NULL, null=True)  # Fixed: added null=True
    move_name = models.CharField(max_length=100)
    score = models.FloatField()
    accuracy = models.FloatField()
    feedback = models.CharField(max_length=20, choices=feedback_choices)
    ai_suggestion = models.TextField(blank=True)
    tested_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tested_time']

    def __str__(self):
        return f"{self.user.username} - {self.move_name} ({self.score})"