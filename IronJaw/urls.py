
from django.contrib import admin
from django.urls import path,include
from IronJaw import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage_view, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('start_free/', views.start_free_view, name='start_free'),
    path('accounts/', include('accounts.urls')),
]
