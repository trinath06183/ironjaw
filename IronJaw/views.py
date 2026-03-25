from django.shortcuts import render

def homepage_view(request):
    return render(request, 'frontpage.html')

def login_view(request):
    return render(request, 'login_page.html')

def start_free_view(request):
    return render(request, 'start_free.html')