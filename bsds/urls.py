from django.urls import path
from . import views

app_name = 'bsds'

urlpatterns = [
    path('', views.bsds_page, name='bsds_page'),
]
