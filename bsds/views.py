from django.shortcuts import render, get_object_or_404
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
    from .models import CoordinatorMemory, CampusCoordinatorConfig
    coordinators = CampusCoordinator.objects.all()
    memories = CoordinatorMemory.objects.all()
    cfg = CampusCoordinatorConfig.objects.first()
    context = {
        'coordinators': coordinators,
        'memories': memories,
        'cfg': cfg,
    }
    return render(request, 'bsds/campus_coordinators.html', context)


def collaboration(request):
    from .models import SponsoredProgram
    universities = Collaboration.objects.filter(collab_type='university')
    clubs = Collaboration.objects.filter(collab_type='club')
    programs = SponsoredProgram.objects.all()
    context = {
        'universities': universities,
        'clubs': clubs,
        'sponsored_programs': programs,
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
    featured_talk = ResearchTalk.objects.filter(order=0).first()
    if featured_talk:
        talks = ResearchTalk.objects.exclude(id=featured_talk.id)
    else:
        talks = ResearchTalk.objects.all()
        
    context = {
        'featured_talk': featured_talk,
        'talks': talks,
    }
    return render(request, 'bsds/research_talks.html', context)


def bsds_event_details(request, pk):
    item = get_object_or_404(BSDSEvent, pk=pk)
    context = {
        'title': item.title,
        'date_text': item.date_text,
        'description': '',
        'details': item.details,
        'apply_url': getattr(item, 'url', None),
        'image_url': item.get_image_url,
    }
    return render(request, 'bsds/details.html', context)


def competition_details(request, pk):
    item = get_object_or_404(Competition, pk=pk)
    context = {
        'title': item.title,
        'date_text': getattr(item, 'year', ''),
        'description': item.description,
        'details': item.details,
        'apply_url': getattr(item, 'apply_url', None),
        'image_url': item.get_image_url,
    }
    return render(request, 'bsds/details.html', context)

