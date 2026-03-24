from django.shortcuts import render
from django.db.models import Prefetch
from .models import ServiceCategory, Service

def service_list(request):
    # Fetch only active services and order them properly
    active_services = Service.objects.filter(is_active=True).order_by('order')
    
    # Prefetch the active services for each category to optimize database hits
    categories = ServiceCategory.objects.prefetch_related(
        Prefetch('services', queryset=active_services)
    ).all()

    context = {
        'categories': categories,
    }
    return render(request, 'service/service_list.html', context)


