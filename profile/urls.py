from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='profile'),
    path('levels/', views.levels, name='levels'),
    path('finance/', views.finance, name='finance'),
    path('id<int:user_id>/', views.user, name='user'),

    path('login/', views.auth_login, name='auth_login'),
]
