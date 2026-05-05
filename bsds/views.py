from django.shortcuts import render
from core.models import BSDSItem
from .models import BSDSEvent, CampusSeminar, SeminarProgramConfig, CampusCoordinator, Collaboration, Competition, ResearchTalk


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


def campus_coordinators(request):
    coordinators = CampusCoordinator.objects.all()
    context = {
        'coordinators': coordinators,
    }
    return render(request, 'bsds/campus_coordinators.html', context)


def collaboration(request):
    universities = Collaboration.objects.filter(collab_type='university')
    clubs = Collaboration.objects.filter(collab_type='club')
    context = {
        'universities': universities,
        'clubs': clubs,
    }
    return render(request, 'bsds/collaboration.html', context)


def competitions(request):
    active_contests = Competition.objects.filter(is_active=True)
    past_winners = Competition.objects.filter(is_active=False)
    context = {
        'active_contests': active_contests,
        'past_winners': past_winners,
    }
    return render(request, 'bsds/competitions.html', context)


def research_talks(request):
    talks = ResearchTalk.objects.all()
    context = {
        'talks': talks,
    }
    return render(request, 'bsds/research_talks.html', context)

