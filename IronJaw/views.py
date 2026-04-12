from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.forms import user_registration_form, fighter_profile_form
from django.contrib.auth.decorators import login_required
from subscriptions.models import subscription
from .utils import fetch_nearby_gyms
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

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
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(email=identifier).first()
        if user_obj:
            username = user_obj.username
        else:
            username = identifier
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
            
    return render(request, 'login_page.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    return render(request, 'startfree.html')

@login_required(login_url='login')
def roadmap_view(request):
    sub = subscription.objects.filter(user=request.user).first()
    if not sub or not sub.is_active():
        return redirect('payment')
    return render(request, 'roadmap.html')

@login_required(login_url='login')
def dashboard_view(request):
    sub = subscription.objects.filter(user=request.user).first()
    has_ai_access = sub.is_active() if sub else False
    return render(request, 'dashboard.html', {'has_ai_access': has_ai_access})

@login_required(login_url='login')
def api_nearby_gyms(request):
    from .utils import fetch_nearby_gyms, geocode_city
    city = request.GET.get('city')
    user_lat = request.GET.get('lat')
    user_lon = request.GET.get('lon')
    
    search_lat = None
    search_lon = None
    
    if city:
        search_lat, search_lon = geocode_city(city)
        if not search_lat or not search_lon:
             return JsonResponse({'error': f'Could not locate {city} on map'}, status=400)
    elif user_lat and user_lon:
        try:
            search_lat = float(user_lat)
            search_lon = float(user_lon)
        except ValueError:
            return JsonResponse({'error': 'Invalid coordinates'}, status=400)
    else:
        return JsonResponse({'error': 'Location not provided'}, status=400)
            
    dist_lat = float(user_lat) if user_lat else search_lat
    dist_lon = float(user_lon) if user_lon else search_lon

    gyms = fetch_nearby_gyms(search_lat, search_lon, ref_lat=dist_lat, ref_lon=dist_lon)
    return JsonResponse({'gyms': gyms})