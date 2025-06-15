from django.urls import path
from . import views



urlpatterns = [
    path('bag/', views.bag, name='bag'),
   
]