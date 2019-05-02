from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from datetime import datetime, timezone, date, time, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, Http404
from e_secretary.forms import *
from django.views import View
import json
from e_secretary.models import *
from e_secretary.tables import *
from django_tables2 import RequestConfig
from django.http import HttpResponse


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
def profile(request, profileID=None):

    profile_id = profileID

    print(profile_id)

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
    user_profile = request.user.profile
    didaskalia = Didaskalia.objects.get(id=didaskalia_id)

    if(user_profile.is_student()):
        if(user_profile.student.parakolouthei(didaskalia_id) is False):
            raise Http404()
    elif(user_profile.is_professor()):
        if(user_profile.professor.didaskei(didaskalia_id) is False):
            raise Http404()

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
    context['didaskalia_id'] = didaskalia_id
    context['user_profile'] = user_profile

    return render(request, 'course.html', context=context)


@login_required
def ergasies(request, didaskalia_id, ergasia_id=None):

    announcements_max = 5
    didaskalia = Didaskalia.objects.get(id=didaskalia_id)
    user_profile = request.user.profile
    drastiriotites = Drastiriotita.objects.filter(
        didaskalia_id=didaskalia)
    ergasies = None
    ergasia = None

    context = {}

    if(user_profile.is_student()):
        if(user_profile.student.parakolouthei(didaskalia_id) is False):
            raise Http404()
        ergasies = SimmetoxiDrastiriotita.objects.filter(
            drastiriotita__in=drastiriotites, student=request.user.profile.student
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
                        ergasia.delivered = True
                        ergasia.save()
    elif(user_profile.is_professor()):
        if(user_profile.professor.didaskei(didaskalia_id) is False):
            raise Http404()
        ergasies = drastiriotites
        if(ergasia_id in ergasies.values_list('id', flat=True)):
            ergasia = Drastiriotita.objects.get(
                id=ergasia_id)
            registered = SimmetoxiDrastiriotita.objects.filter(
                drastiriotita=ergasia)
            context['registered'] = registered

            if(request.method == 'POST'):
                form = GradeUploadForm(request.POST)
                if form.is_valid():
                    if(form.cleaned_data['grade'] and form.cleaned_data['student_id']):
                        ergasia_foititi = SimmetoxiDrastiriotita.objects.get(
                            drastiriotita=ergasia, student=Student.objects.get(am=int(form.cleaned_data['student_id'])))
                        ergasia_foititi.grade = form.cleaned_data['grade']
                        ergasia_foititi.save()

    context['didaskalia'] = didaskalia
    context['ergasies'] = ergasies
    context['ergasia'] = ergasia
    context['didaskalia_id'] = didaskalia_id

    return render(request, 'ergasies.html', context=context)


@login_required
def new_ergasia(request, didaskalia_id):
    user_profile = request.user.profile
    if(user_profile.professor.didaskei(didaskalia_id) is False):
        raise Http404()

    didaskalia = Didaskalia.objects.get(id=didaskalia_id)
    diloseis = Dilosi.objects.filter(didaskalia=didaskalia)

    if request.method == 'GET':
        form = NewErgasiaForm()
    elif request.method == 'POST':
        form = NewErgasiaForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            sintelestis = form.cleaned_data['sintelestis']
            due_date = form.cleaned_data['due_date']
            tipos = form.cleaned_data['tipos']
            perigrafi = form.cleaned_data['perigrafi']
            if(form.cleaned_data['file']):
                file = form.cleaned_data['file']
            else:
                file = None
            new_drastiriotita = Drastiriotita.objects.create(
                title=title, sintelestis=sintelestis, due_date=due_date, tipos=tipos, perigrafi=perigrafi, file=file, didaskalia=didaskalia)
            for dilosi in diloseis:
                new_simmetoxi = SimmetoxiDrastiriotita.objects.create(
                    drastiriotita=new_drastiriotita, student=dilosi.student)
            return HttpResponseRedirect(reverse('ergasies', kwargs={'didaskalia_id': didaskalia_id},))

    context = {
        'form': form,
    }

    return render(request, 'new_ergasia.html', context=context)

@login_required
def new_announcement(request, didaskalia_id):

    user_profile = request.user.profile

    if(not user_profile.is_professor()):
        raise Http404()

    if(user_profile.professor.didaskei(didaskalia_id) is False):
        raise Http404()

    didaskalia = Didaskalia.objects.get(id=didaskalia_id)

    if request.method == 'GET':
        form = NewAnnouncementForm()
    elif request.method == 'POST':
        form = NewAnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.cleaned_data['content']

            new_announcement = Announcement.objects.create(
                content=content, didaskalia_id=didaskalia)
            return HttpResponseRedirect(reverse('course', kwargs={'didaskalia_id': didaskalia_id},))

    context = {
        'form': form,
        'didaskalia': didaskalia,
        'didaskalia_id': didaskalia_id
    }

    return render(request, 'new_announcement.html', context=context)


def next_weekday(weekday):
    d = datetime.now()
    days_ahead = weekday - d.weekday()
    # if days_ahead <= 0:  # Target day already happened this week
    #     days_ahead += 7
    return d + timedelta(days_ahead)


@login_required
def orologio(request):

    user_profile = request.user.profile

    if(user_profile.is_student()):
        diloseis = Dilosi.objects.filter(
            student=user_profile.student)
        didaskalies = [dilosi.didaskalia for dilosi in diloseis]
    elif(user_profile.is_professor()):
        didaskalies = user_profile.professor.didaskalia.all()

    programma = Orologio.objects.filter(didaskalia__in=didaskalies)

    orologio = []

    for mathima in programma:

        start_datetime = next_weekday(mathima.DAYS_CHOICES_INT[mathima.day]).strftime(
            '%d-%m-%Y') + ' ' + mathima.start_time.strftime('%H:%M:%S')

        end_datetime = next_weekday(mathima.DAYS_CHOICES_INT[mathima.day]).strftime(
            '%d-%m-%Y') + ' ' + (mathima.end_time).strftime('%H:%M:%S')

        orologio.append({
            "id": mathima.didaskalia.id,
            "title": mathima.didaskalia.name(),
            "start": start_datetime,
            "end": end_datetime,
            "backgroundColor": '#039BE5',
            "textColor": '#FFF'
        })

    orologio = json.dumps(orologio,  ensure_ascii=False)

    context = {
        'orologio': orologio
    }

    return render(request, 'orologio.html', context=context)
  
@login_required  
def diloseis(request):

    didaskalies_data = Didaskalia.objects.raw('select e_secretary_didaskalia.id,e_secretary_course.name, e_secretary_course.tomeas, e_secretary_course.ects,e_secretary_course.programma_spoudwn,e_secretary_course.ipoxrewtiko from e_secretary_course join e_secretary_didaskalia on e_secretary_course.id = e_secretary_didaskalia.course_id where e_secretary_didaskalia.akad_etos = YEAR(CURDATE());')

    am = request.user.profile.get_am()

    dilosi_data = Didaskalia.objects.raw('select e_secretary_didaskalia.id, e_secretary_course.name, e_secretary_course.tomeas, e_secretary_course.ects from (e_secretary_dilosi join e_secretary_didaskalia on e_secretary_dilosi.didaskalia_id = e_secretary_didaskalia.id) join e_secretary_course on e_secretary_didaskalia.course_id = e_secretary_course.id where e_secretary_dilosi.student_id = {};'.format(am))

    dilosi_table = DilosiTable(dilosi_data)
    didaskalies_table = DidaskaliesTable(didaskalies_data)

    if request.is_ajax():
        Dilosi.objects.filter(student = am).delete()
        request_data = request.POST.getlist("dilosi[]")
        for x in request_data:
            student = Student.objects.get(am = am)
            didaskalia = Didaskalia.objects.get(id = x)
            q = Dilosi(student=student,didaskalia=didaskalia)
            q.save()
        return HttpResponse("OK")

    context = {
        'didaskalies_table' : didaskalies_table,
        'dilosi_table': dilosi_table,
    }

    return render(request, 'diloseis.html', context=context)