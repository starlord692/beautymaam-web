from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('api/slots/', views.get_available_slots, name='get_slots'),
]
