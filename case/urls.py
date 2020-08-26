from django.urls import path
from . import views

urlpatterns = [
    path('<int:card_id>/', views.case, name='case'),
]
