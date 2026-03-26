from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import user_registration_form, fighter_profile_form

def register_view(request):
    if request.method == 'POST':
        user_form = user_registration_form(request.POST)
        profile_form = fighter_profile_form(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            login(request,user)
            return redirect('login')
    else:
        user_form = user_registration_form()
        profile_form = fighter_profile_form()
    return render(request, "start_free.html", {'user_form': user_form, 'profile_form': profile_form})