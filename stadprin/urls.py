from django.urls import path
from . import views

# Define webapp name
app_name = 'stadprin'

urlpatterns = [
    path('', views.index, name='home'),  # Index(home) page
    path('5chKFC/', views.gantt_chart, name='apd_gantt'),  # Contact page
]
