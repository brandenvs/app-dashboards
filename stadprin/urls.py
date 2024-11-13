from django.urls import path
from . import views

# Define webapp name
app_name = 'stadprin'

urlpatterns = [
    path('', views.index, name='home'),  # Index(home) page
    path('career/', views.career, name='career'),  # Career page
    path('contact/', views.contact, name='contact'),  # Contact page
    
]
