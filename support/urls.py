from django.urls import path
from . import views

urlpatterns = [
    path('', views.support, name='support_url'),
    path('send_message/', views.send_message, name='send_message_url'),
    path('privacy/', views.privacy, name='privacy_url'),
    path('terms/', views.terms, name='terms_url'),
]
