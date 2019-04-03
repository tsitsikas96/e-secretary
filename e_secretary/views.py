from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, Http404
from e_secretary.forms import ChangeAvatarForm, FileUploadForm
from django.views import View

from e_secretary.models import *


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
        'events': events,
        'announcements': announcements,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


@login_required
def profile(request):

    profile_id = request.GET.get('profile_id')

    if (profile_id is None):
        user = request.user
    else:
        profile_obj = Profile.objects.get(id=profile_id)
        user = profile_obj.user

    profile_id = user.profile

    context = {
        'profile_id': profile_id,
    }

    return render(request, 'profile.html', context=context)


@login_required
def change_avatar(request):

    profile_instance = request.user.profile

    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES)

        if form.is_valid():
            if(form.cleaned_data['delete_photo']):
                profile_instance.photo.delete(save=True)
            elif(form.cleaned_data['photo']):
                profile_instance.photo = form.cleaned_data['photo']
                profile_instance.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = ChangeAvatarForm()

    context = {
        'form': form,
        'profile_instance': profile_instance,
    }

    return render(request, 'change_avatar.html', context=context)


@login_required
def my_courses(request):

    announcements_max = 5
    didaskalies_max = 5

    context = {}

    if request.method == 'GET':
        didaskalies_list = request.user.profile.get_my_courses()
        didaskalies_paginator = Paginator(didaskalies_list, didaskalies_max)
        didaskalies_page = request.GET.get('didaskalies_page') or 1
        didaskalies = didaskalies_paginator.get_page(didaskalies_page)
        didaskalies_page_counter = didaskalies_max*(int(didaskalies_page)-1)

        announcements_list = Announcement.objects.filter(
            didaskalia_id__in=didaskalies_list)
        announcements_paginator = Paginator(
            announcements_list, announcements_max)
        announcements_page = request.GET.get('announcements_page') or 1
        announcements = announcements_paginator.get_page(announcements_page)
        announcements_page_counter = announcements_max * \
            (int(announcements_page)-1)

        context['didaskalies'] = didaskalies
        context['didaskalies_page_counter'] = didaskalies_page_counter
        context['announcements'] = announcements
        context['announcements_page_counter'] = announcements_page_counter

    return render(request, 'my_courses.html', context=context)


@login_required
def course(request, didaskalia_id):

    announcements_max = 5

    didaskalia = Didaskalia.objects.get(id=didaskalia_id)

    if(request.user.profile.student.parakolouthei(didaskalia_id) is False):
        raise Http404("")

    announcements_list = Announcement.objects.filter(
        didaskalia_id=didaskalia)
    announcements_paginator = Paginator(
        announcements_list, announcements_max)
    announcements_page = request.GET.get('announcements_page') or 1
    announcements = announcements_paginator.get_page(announcements_page)
    announcements_page_counter = announcements_max * \
        (int(announcements_page)-1)

    context = {
        'didaskalia': didaskalia,
    }
    context['announcements'] = announcements
    context['announcements_page_counter'] = announcements_page_counter

    return render(request, 'course.html', context=context)


@login_required
def ergasies(request, didaskalia_id, ergasia_id=None):

    announcements_max = 5
    ergasia = None

    if(request.user.profile.student.parakolouthei(didaskalia_id) is False):
        raise Http404()

    didaskalia = Didaskalia.objects.get(id=didaskalia_id)
    user_profile = request.user.profile
    drastiriotites = Drastiriotita.objects.filter(
        didaskalia_id=didaskalia, tipos=Drastiriotita.ERGASIA)
    ergasies = None
    ergasies = SimmetoxiDrastiriotita.objects.filter(
        id__in=drastiriotites, student=request.user.profile.student
    )

    if(ergasia_id in ergasies.values_list('id', flat=True)):
        ergasia = SimmetoxiDrastiriotita.objects.get(
            id=ergasia_id, student=request.user.profile.student)
        if(request.method == 'POST'):
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                if(form.cleaned_data['file']):
                    ergasia.file.delete(save=True)
                    ergasia.file = form.cleaned_data['file']
                    ergasia.save()

    context = {
        'didaskalia': didaskalia,
        'ergasies': ergasies,
        'ergasia': ergasia,
    }

    return render(request, 'ergasies.html', context=context)
