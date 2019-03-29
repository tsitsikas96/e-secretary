from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import datetime, timezone

# Create your views here.

from e_secretary.models import Event, Secr_Announcement


def index(request):

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
        'is_student': True,
        'events': events,
        'announcements': announcements
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
