from django.urls import path
from . import views

# Define webapp name
app_name = 'portal'

urlpatterns = [
    path('', views.index, name='index'),
    path('new-app/', views.create_app, name='create_app'),
]