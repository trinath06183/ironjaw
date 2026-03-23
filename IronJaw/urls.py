
from django.contrib import admin
from django.urls import path
from IronJaw import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage_view, name='homepage'),
    path('login/', views.login_view, name='login'),
]
