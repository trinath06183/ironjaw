from django.shortcuts import render
from accounts.forms import user_registration_form, fighter_profile_form

# def homepage_view(request):
#     return render(request, 'frontpage.html')

# def login_view(request):
#     return render(request, 'login_page.html')

# def start_free_view(request):
#     user_form = user_registration_form()
#     profile_form = fighter_profile_form()
#     return render(request, 'start_free.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })


def home(request):
    return render(request, 'home.html' )

def login_view(request):
    return render(request, 'login_page.html')

def register_view(request):
    return render(request, 'startfree.html')

def roadmap_view(request):
    return render(request, 'roadmap.html')