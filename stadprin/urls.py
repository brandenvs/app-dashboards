from django.urls import path
from . import views

# Define webapp name
app_name = 'stadprin'

urlpatterns = [
    path('', views.temp, name='temp'),
]