from django.urls import path
from . import views

# Setting the app namespace
app_name = 'service'

urlpatterns = [
    # Route for the main services page
    path('', views.service_list, name='service_list'),
    path('clinical/', views.clinical_service_list, name='clinical_service_list'),
    path('clinical/<slug:slug>/', views.clinical_service_detail, name='clinical_service_detail'),
    path('<slug:slug>/', views.service_detail, name='service_detail'),
]