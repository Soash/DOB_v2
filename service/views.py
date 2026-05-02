from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import ServiceCategory, Service, ClinicalService

def service_list(request):
    # Fetch core services (is_top=True)
    top_services = Service.objects.filter(is_active=True, is_top=True).order_by('order')

    # Fetch only active services and order them properly
    active_services = Service.objects.filter(is_active=True).order_by('order')
    
    # Prefetch the active services for each category to optimize database hits
    categories = ServiceCategory.objects.prefetch_related(
        Prefetch('services', queryset=active_services)
    ).all()

    context = {
        'top_services': top_services,
        'categories': categories,
    }
    return render(request, 'service/service_list.html', context)

def service_detail(request, slug):
    # Fetch the service, optimizing by prefetching related images and FAQs
    service = get_object_or_404(
        Service.objects.prefetch_related('images', 'faqs'), 
        slug=slug, 
        is_active=True
    )

    context = {
        'service': service,
    }
    return render(request, 'service/service_detail.html', context)

def clinical_service_list(request):
    services = ClinicalService.objects.filter(is_active=True).order_by('order')
    context = {
        'services': services,
    }
    return render(request, 'service/clinical_service_list.html', context)

def clinical_service_detail(request, slug):
    service = get_object_or_404(
        ClinicalService.objects.prefetch_related('images', 'faqs'),
        slug=slug,
        is_active=True
    )
    context = {
        'service': service,
    }
    return render(request, 'service/clinical_service_detail.html', context)
