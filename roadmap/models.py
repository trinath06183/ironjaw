from django.db import models
from django.contrib.auth.models import User
from fighting_style.models import fighting_style  


class ai_roadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fight_style = models.ForeignKey(fighting_style, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    generates_plan = models.JSONField()
    duration = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Roadmap — {self.title}"


class roadmap_steps(models.Model):
    roadmap = models.ForeignKey(ai_roadmap, on_delete=models.CASCADE)
    week = models.IntegerField()
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['week', 'order']

    def __str__(self):
        return f"Week {self.week} - Step {self.order} - {self.title}"  