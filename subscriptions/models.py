from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class subscription(models.Model):
    plan_choices=[
        ('free','Free'),
        ('paid','Paid'),
    ]
    status_choices=[
        ('active','Active'),
        ('pending','Pending'),
        ('expired','Expired'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=100,choices=plan_choices)
    subscription_start_date = models.DateTimeField(auto_now_add=True)
    subscription_end_date = models.DateTimeField()
    payment_status= models.CharField(max_length=10,choices=status_choices)
    
    def is_active(self):
        from datetime import date
        return self.subscription_type == 'paid' and self.subscription_end_date >= date.today()   
    
    def __str__(self):
        return f"{self.user.username}'s Subscription — {self.subscription_type}"
