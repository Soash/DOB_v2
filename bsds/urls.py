from django.urls import path
from . import views

app_name = 'bsds'

urlpatterns = [
    path('', views.bsds_page, name='bsds_page'),
    path('on-campus-seminar/', views.on_campus_seminar, name='on_campus_seminar'),
]
