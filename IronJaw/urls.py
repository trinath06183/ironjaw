
from django.contrib import admin
from django.urls import path,include
from IronJaw import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('accounts/', include('accounts.urls')),
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
