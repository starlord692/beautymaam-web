from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.service_list, name='home'), # Redirect or main dashboard
    path('services/', views.service_list, name='services'),
    path('settings/', views.settings_view, name='settings'),
]
