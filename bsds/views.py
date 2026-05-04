from django.shortcuts import render
from core.models import BSDSItem
from .models import BSDSEvent, CampusSeminar, SeminarProgramConfig


def bsds_page(request):
    bsds_items = BSDSItem.objects.filter(is_active=True).order_by('order')
    events = BSDSEvent.objects.all()

    context = {
        'bsds_items': bsds_items,
        'events': events,
    }
    return render(request, 'bsds/bsds.html', context)


def on_campus_seminar(request):
    campuses = CampusSeminar.objects.all()
    # Build JSON-safe list for the JS gallery
    import json
    campuses_json = json.dumps([
        {
            'name': c.abbreviation,
            'title': c.university_name,
            'desc': c.event_description,
            'img': c.get_image_url,
        }
        for c in campuses
    ])
    context = {
        'campuses': campuses,
        'campuses_json': campuses_json,
        'cfg': SeminarProgramConfig.objects.first(),
    }
    return render(request, 'bsds/on_campus_seminar.html', context)

