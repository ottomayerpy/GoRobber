from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_url'),
    path('rating/', views.rating, name='rating_url'),
    path('payouts/', views.payouts, name='payouts_url'),
]
