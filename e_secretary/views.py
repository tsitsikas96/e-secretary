from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from e_secretary.models import *
from django.conf import settings


def index(request):

    static_url = settings.STATIC_URL

    event_list = Event.objects.all()
    event_paginator = Paginator(event_list, 3)

    event_page = request.GET.get('page')
    events = event_paginator.get_page(event_page)

    for event in events:
        if(event.date.replace(tzinfo=None) < datetime.now()):
            event.old = True

    announcements_list = Secr_Announcement.objects.all()
    announcements_paginator = Paginator(announcements_list, 6)
    announcements_page = request.GET.get('announcements_page')
    announcements = announcements_paginator.get_page(announcements_page)

    context = {
        'events': events,
        'announcements': announcements,
        'STATIC_URL': static_url
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


@login_required
def profile(request):

    static_url = settings.STATIC_URL

    idiotita = None
    is_student = False
    is_professor = False
    is_grammateia = False
    user = None
    temp = None
    etos = None

    profile_id = request.GET.get('profile_id')

    if (profile_id is None):
        user = request.user
    else:
        profile_obj = Profile.objects.get(id=profile_id)
        user = profile_obj.user

    if (user.groups.filter(name__in=['Students']).exists()):
        idiotita = "Φοιτητής"
        is_student = True
        etos = abs(datetime.now().year -
                   user.profile.student.date_eisagwghs.year) + 1
    elif (user.groups.filter(name__in=['Professor']).exists()):
        idiotita = user.profile.professor.get_title_display()
        is_professor = True
    elif (user.profile.grammateia):
        idiotita = "Γραμματεία"
        is_grammateia = True

    profile_id = user.profile

    context = {
        'STATIC_URL': static_url,
        'idiotita': idiotita,
        'is_grammateia': is_grammateia,
        'is_student': is_student,
        'is_professor': is_professor,
        'profile_id': profile_id,
        'etos': etos,
    }

    return render(request, 'profile.html', context=context)
