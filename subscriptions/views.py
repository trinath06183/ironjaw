from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import subscription
from django.contrib import messages

@login_required(login_url='login')
def payment_view(request):
    if request.method == 'POST':
        # Simulate payment processing
        sub, created = subscription.objects.get_or_create(
            user=request.user,
            defaults={
                'subscription_type': 'paid',
                'subscription_end_date': timezone.now() + timedelta(days=30),
                'payment_status': 'pending'
            }
        )
        if not created:
            # Update existing subscription
            sub.subscription_type = 'paid'
            sub.payment_status = 'pending'
            sub.subscription_end_date = timezone.now() + timedelta(days=30)
            sub.save()
            
        messages.success(request, 'Payment submitted successfully! Please wait for admin approval.')
        return redirect('dashboard')
        
    return render(request, 'payment.html')
