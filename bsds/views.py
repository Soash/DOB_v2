from django.shortcuts import render
from core.models import BSDSItem
from .models import BSDSEvent


def bsds_page(request):
    bsds_items = BSDSItem.objects.filter(is_active=True).order_by('order')
    events = BSDSEvent.objects.all()

    context = {
        'bsds_items': bsds_items,
        'events': events,
    }
    return render(request, 'bsds/bsds.html', context)
