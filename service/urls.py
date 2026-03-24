from django.urls import path
from . import views

# Setting the app namespace
app_name = 'service'

urlpatterns = [
    # Route for the main services page
    path('', views.service_list, name='service_list'),
]