from django.shortcuts import render
from django.db import models
from .models import BSDSItem
from service.models import ServiceCategory
from django.contrib.auth import get_user_model

def home(request):
    User = get_user_model()
    
    # Fetch some featured services (e.g., top 4 from the first few categories)
    # This is just an example of grabbing a subset of services to highlight
    categories = ServiceCategory.objects.prefetch_related('services')[:3]
    featured_services = []
    for cat in categories:
        featured_services.extend(list(cat.services.all()[:2]))
    featured_services = featured_services[:6] # Limit to 6
    
    # Fetch some active BSDS items (top 3)
    bsds_items = BSDSItem.objects.filter(is_active=True).order_by('order')[:3]
    
    # Quick stats
    team_count = User.objects.filter(is_active=True, is_staff=True).count()
    services_count = ServiceCategory.objects.aggregate(total=models.Count('services'))['total'] or 30
    
    context = {
        'featured_services': featured_services,
        'bsds_items': bsds_items,
        'team_count': team_count,
        'services_count': services_count,
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