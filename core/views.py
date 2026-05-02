from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import BSDSItem, ResearchPaper, BlogPost
from service.models import ServiceCategory, Service
from django.contrib.auth import get_user_model

def home(request):
    User = get_user_model()
    
    # Fetch the top services directly using the new is_top flag
    featured_services = Service.objects.select_related('category').filter(is_active=True, is_top=True).order_by('order')[:5]
    
    # Fetch some active BSDS items (top 3)
    bsds_items = BSDSItem.objects.filter(is_active=True).order_by('order')[:3]
    
    # Quick stats
    team_count = User.objects.filter(is_active=True, is_staff=True).count()
    services_count = ServiceCategory.objects.aggregate(total=models.Count('services'))['total'] or 30
    
    # Recent Research and Blog Posts
    recent_papers = ResearchPaper.objects.all()[:5]
    recent_blogs = BlogPost.objects.filter(published=True)[:5]
    
    # Fetch categories and their active services for the tabbed section
    from django.db.models import Prefetch
    active_services = Service.objects.filter(is_active=True).order_by('order')
    categories = ServiceCategory.objects.prefetch_related(
        Prefetch('services', queryset=active_services)
    ).all()
    
    # Fetch clinical services for the homepage carousel
    from service.models import ClinicalService
    clinical_services = ClinicalService.objects.filter(is_active=True).order_by('order')
    
    context = {
        'featured_services': featured_services,
        'bsds_items': bsds_items,
        'team_count': team_count,
        'services_count': services_count,
        'recent_papers': recent_papers,
        'recent_blogs': recent_blogs,
        'categories': categories,
        'clinical_services': clinical_services,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')


def bsds_page(request):
    # Fetch all active BSDS items
    bsds_items = BSDSItem.objects.filter(is_active=True).order_by('order')
    
    context = {
        'bsds_items': bsds_items,
    }
    return render(request, 'core/bsds.html', context)

from django.contrib.auth import get_user_model

def dhaka_branch(request):
    return render(request, 'core/dhaka_branch.html')

def chittagong_branch(request):
    return render(request, 'core/chittagong_branch.html')

from django.db.models import Prefetch

def team(request):
    User = get_user_model()
    from users.models import Department
    
    # We want to fetch all departments, ordered by 'order', 
    # and prefetch their active staff users ordered by 'order_in_department'
    active_users = User.objects.filter(is_active=True, is_staff=True).order_by('order_in_department')
    
    departments = Department.objects.prefetch_related(
        Prefetch('users', queryset=active_users)
    ).order_by('order', 'name')
    
    context = {
        'departments': departments,
    }
    return render(request, 'core/team.html', context)

def coming_soon(request):
    return render(request, 'core/coming_soon.html')

def research_papers(request):
    papers = ResearchPaper.objects.all()
    return render(request, 'core/research_papers.html', {'papers': papers})

def blog(request):
    posts = BlogPost.objects.filter(published=True)
    return render(request, 'core/blog.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, 'core/blog_detail.html', {'post': post})