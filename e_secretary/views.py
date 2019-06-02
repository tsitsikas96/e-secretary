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
        context = {}
        didaskalies_list = request.user.profile.get_my_courses()
        if(didaskalies_list):
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

    didaskalies = None

    if(user_profile.is_student()):
        diloseis = Dilosi.objects.filter(student=user_profile.student)
        didaskalies = [dilosi.didaskalia for dilosi in diloseis]
    elif(user_profile.is_professor()):
        didaskalies = user_profile.professor.didaskalia.all()

    if(didaskalies):
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
    else:
        context = {}

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

@login_required  
def vathmologies(request):
    user_profile = request.user.profile
    if(user_profile.is_professor()):
        didaskalies_prof= Didaskalia.objects.raw('select e_secretary_professor_didaskalia.didaskalia_id as id,e_secretary_course.name,e_secretary_didaskalia.akad_etos from (e_secretary_professor_didaskalia join e_secretary_didaskalia on e_secretary_professor_didaskalia.didaskalia_id = e_secretary_didaskalia.id) join e_secretary_course on e_secretary_course.id = e_secretary_didaskalia.course_id;')

        didaskalies_ids = {}
        for x in didaskalies_prof:
            tag = x.name + ' ' + str(x.akad_etos)
            didaskalies_ids[tag] = x.id

        vathmologies_data = {}
        
        template = 'vathmologies.html'
        if request.is_ajax():
            if request.POST.get('text'):
                request_data = request.POST.get('text')
                vathmologies_data = SimmetoxiDrastiriotita.objects.raw(
                    'SELECT id, ergasies, proodos, lab, exams,  ROUND(ROUND( ROUND(COALESCE(ergasies_with_weight, 0) + COALESCE(proodos_with_weight, 0) + COALESCE(lab_with_weight, 0) + COALESCE(exams_with_weight, 0),1) * 2,0) / 2,1) AS telikos FROM (SELECT         e_secretary_simmetoxidrastiriotita.student_id as id, AVG(CASE WHEN e_secretary_drastiriotita.tipos = "ERGASIA" THEN e_secretary_simmetoxidrastiriotita.grade END) AS ergasies, AVG(CASE WHEN e_secretary_drastiriotita.tipos = "PROODOS" THEN e_secretary_simmetoxidrastiriotita.grade END ) AS proodos, AVG(CASE WHEN e_secretary_drastiriotita.tipos = "ERGASTIRIO" THEN e_secretary_simmetoxidrastiriotita.grade END) AS lab, AVG(CASE WHEN e_secretary_drastiriotita.tipos = "EKSTETASTIKI" THEN e_secretary_simmetoxidrastiriotita.grade END) AS exams, AVG(CASE WHEN e_secretary_drastiriotita.tipos = "ERGASIA" THEN IF(e_secretary_simmetoxidrastiriotita.grade >= 5,e_secretary_simmetoxidrastiriotita.grade,0) * e_secretary_drastiriotita.sintelestis END) AS ergasies_with_weight,AVG(CASE WHEN e_secretary_drastiriotita.tipos = "PROODOS" THEN IF(e_secretary_simmetoxidrastiriotita.grade >= 5,e_secretary_simmetoxidrastiriotita.grade,0) * e_secretary_drastiriotita.sintelestis END) AS proodos_with_weight,AVG(CASE WHEN e_secretary_drastiriotita.tipos = "ERGASTIRIO" THEN IF(e_secretary_simmetoxidrastiriotita.grade >= 5,e_secretary_simmetoxidrastiriotita.grade,0) * e_secretary_drastiriotita.sintelestis END) AS lab_with_weight,AVG(CASE WHEN e_secretary_drastiriotita.tipos = "EKSTETASTIKI" THEN IF(e_secretary_simmetoxidrastiriotita.grade >= 5,e_secretary_simmetoxidrastiriotita.grade,0) * e_secretary_drastiriotita.sintelestis END) AS exams_with_weight FROM `e_secretary_simmetoxidrastiriotita` JOIN e_secretary_drastiriotita ON e_secretary_simmetoxidrastiriotita.drastiriotita_id = e_secretary_drastiriotita.id WHERE e_secretary_drastiriotita.didaskalia_id = {} GROUP BY e_secretary_simmetoxidrastiriotita.student_id) AS t'.format(didaskalies_ids[request_data])
                )

                template = 'vathmologies_prof_table.html'
                vathmologies_table = VathmologiesProfTable(vathmologies_data)
                context = {
                    'vathmologies_table_prof': vathmologies_table,
                }

                return render(request,template,context)
            elif request.POST.get('save'):
                for x in didaskalies_ids:
                    vathmologies_data = SimmetoxiDrastiriotita.objects.raw(
                    'SELECT id,  ROUND(ROUND( ROUND(COALESCE(ergasies_with_weight, 0) + COALESCE(proodos_with_weight, 0) + COALESCE(lab_with_weight, 0) + COALESCE(exams_with_weight, 0),1) * 2,0) / 2,1) AS telikos FROM (SELECT e_secretary_simmetoxidrastiriotita.student_id as id, AVG(CASE WHEN e_secretary_drastiriotita.tipos = "ERGASIA" THEN IF(e_secretary_simmetoxidrastiriotita.grade >= 5,e_secretary_simmetoxidrastiriotita.grade,0) * e_secretary_drastiriotita.sintelestis END) AS ergasies_with_weight,AVG(CASE WHEN e_secretary_drastiriotita.tipos = "PROODOS" THEN IF(e_secretary_simmetoxidrastiriotita.grade >= 5,e_secretary_simmetoxidrastiriotita.grade,0) * e_secretary_drastiriotita.sintelestis END) AS proodos_with_weight,AVG(CASE WHEN e_secretary_drastiriotita.tipos = "ERGASTIRIO" THEN IF(e_secretary_simmetoxidrastiriotita.grade >= 5,e_secretary_simmetoxidrastiriotita.grade,0) * e_secretary_drastiriotita.sintelestis END) AS lab_with_weight,AVG(CASE WHEN e_secretary_drastiriotita.tipos = "EKSTETASTIKI" THEN IF(e_secretary_simmetoxidrastiriotita.grade >= 5,e_secretary_simmetoxidrastiriotita.grade,0) * e_secretary_drastiriotita.sintelestis END) AS exams_with_weight FROM `e_secretary_simmetoxidrastiriotita` JOIN e_secretary_drastiriotita ON e_secretary_simmetoxidrastiriotita.drastiriotita_id = e_secretary_drastiriotita.id WHERE e_secretary_drastiriotita.didaskalia_id = {} GROUP BY     e_secretary_simmetoxidrastiriotita.student_id) AS t'.format(didaskalies_ids[x])
                    )
                    for y in vathmologies_data:
                        Dilosi.objects.filter(student_id=y.id,didaskalia_id = didaskalies_ids[x]).update(telikos_vathmos=y.telikos)

        vathmologies_table = VathmologiesProfTable(vathmologies_data)
        context = {
            'didaskalies_prof' : didaskalies_prof,
            'vathmologies_table_prof': vathmologies_table,
        }
        return render(request,template,context)
    elif(user_profile.is_student()):
        am = request.user.profile.get_am()

        vathmologies_data = Dilosi.objects.raw('SELECT e_secretary_dilosi.didaskalia_id as id, e_secretary_course.name,e_secretary_didaskalia.akad_etos,e_secretary_dilosi.telikos_vathmos FROM (e_secretary_dilosi join e_secretary_didaskalia on e_secretary_dilosi.didaskalia_id = e_secretary_didaskalia.id) join e_secretary_course on e_secretary_didaskalia.course_id = e_secretary_course.id where e_secretary_dilosi.student_id = {} ORDER BY e_secretary_didaskalia.akad_etos DESC, e_secretary_course.name;'.format(am))
        
        vathmologies_table = VathmologiesStudTable(vathmologies_data)
        template = "vathmologies.html"
        context = {
            'vathmologies_table_stud': vathmologies_table,
        }
        return render(request,template,context)

    return render(request,'vathmologies.html',{})

@login_required  
def certificates(request):
    user_profile = request.user.profile
    form = CertificateForm()
    am = user_profile.get_am()
    student = Student.objects.get(am=am)
    table_data = Certificate.objects.filter(student_am_id = am)
    table = CertificatesTable(table_data)

    if request.method == 'POST':
        submit_form = CertificateForm(request.POST)
        if submit_form.is_valid():
            
            tipos = submit_form.cleaned_data['tipos']
            copies = submit_form.cleaned_data['copies']
            student_am = student
            Certificate.objects.create(cert_type=tipos,copies=copies,student_am = student_am)
            
        return HttpResponseRedirect('/certificates/')
    
    context = {'form' : form, 'table':table}
    return render(request,"certificates.html",context)