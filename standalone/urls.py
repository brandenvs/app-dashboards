from django.urls import path
from . import views

# Define webapp name
app_name = 'standalone'

urlpatterns = [
    path('progression-tracker/', views.progression_tracker, name='progression_tracker'), 
]