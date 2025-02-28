from django.urls import path
from . import views

# Define webapp name
app_name = 'standalone'

urlpatterns = [
    # path('progression-tracker/', views.progression_tracker, name='progression_tracker'),
    path('bt-bot/', views.bt_bot, name='bt_bot'),
    path('exchange-data-api/', views.exchange_data_api, name='exchange_data_api'),
    # path('home/', views.index, name='home'),
]