from django.urls import path
from . import views

app_name = 'bsds'

urlpatterns = [
    path('', views.bsds_page, name='bsds_page'),
    path('on-campus-seminar/', views.on_campus_seminar, name='on_campus_seminar'),
    path('campus-coordinators/', views.campus_coordinators, name='campus_coordinators'),
    path('collaboration/', views.collaboration, name='collaboration'),
    path('competitions/', views.competitions, name='competitions'),
    path('research-talks/', views.research_talks, name='research_talks'),
]
