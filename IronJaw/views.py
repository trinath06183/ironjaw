from django.shortcuts import render

def homepage_view(request):
    return render(request, 'homepage.html')

def login_view(request):
    return render(request, 'login.html')
