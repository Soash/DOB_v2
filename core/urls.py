from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('bsds/', views.bsds_page, name='bsds_page'),
    path('branches/dhaka/', views.dhaka_branch, name='dhaka_branch'),
    path('branches/chittagong/', views.chittagong_branch, name='chittagong_branch'),
    path('team/', views.team, name='team'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
    path('research/', views.research_papers, name='research_papers'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]
