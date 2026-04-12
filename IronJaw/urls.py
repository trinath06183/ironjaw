
from django.contrib import admin
from django.urls import path,include
from IronJaw import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('accounts/', include('accounts.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/nearby-gyms/', views.api_nearby_gyms, name='api_nearby_gyms'),
]
