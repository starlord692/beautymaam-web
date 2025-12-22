from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('gallery/', views.GalleryView.as_view(), name='act_gallery'), # Changed name to avoid conflict with static 'gallery' URL logic if any
    path('contact/', views.contact, name='contact'),
]
