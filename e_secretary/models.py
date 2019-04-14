from django.db import models
from django.urls import reverse
from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
# YOLO


class Course(models.Model):

    HMTY_Bachelor = 'HMTY_Bachelor'
    HMTY_Masters = 'HMTY_Masters'

    PROGRAMMA_SPOUDWN_CHOICES = (
        (HMTY_Bachelor, 'HMTY_Bachelor'),
        (HMTY_Masters, 'HMTY_Masters')
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, help_text='Course Name')
    tomeas = models.CharField(max_length=100, help_text='Tomeas Name')
    ects = models.IntegerField()
    programma_spoudwn = models.CharField(
        max_length=45, choices=PROGRAMMA_SPOUDWN_CHOICES, help_text='Programma Spoudwn')
    ipoxrewtiko = models.BooleanField()

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Course."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'{self.name}'


class Didaskalia(models.Model):
    EARINO = 'EARINO'
    XEIMERINO = 'XEIMERINO'

    YEAR_CHOICES = (
        (EARINO, 'EARINO'),
        (XEIMERINO, 'XEIMERINO')
    )
    SEMESTER_CHOICES = ((y, y)
                        for y in range(1968, datetime.now().year+1))
    # Fields
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    akad_etos = models.IntegerField(choices=SEMESTER_CHOICES,
                                    default=datetime.now().year)
    eksamino = models.CharField(max_length=9, choices=YEAR_CHOICES)
    perigrafi = models.TextField(null=True, blank=True)

    # Metadata
    class Meta:
        ordering = ['akad_etos']

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'{self.id} - {self.get_name()}'

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Course."""
        return reverse('model-detail-view', args=[str(self.id)])

    def get_professors(self):
        return Professor.objects.filter(didaskalia=self.id).all()

    def get_announcements(self):
        return Announcement.objects.filter(didaskalia_id=self.id)

    def get_name(self):
        return self.course.name


class Orologio(models.Model):
    MON = 'MON'
    TUE = 'TUE'
    WEN = 'WEN'
    THU = 'THU'
    FRI = 'FRI'
    SAT = 'SAT'
    SUN = 'SUN'

    DAYS_CHOICES = (
        (MON, 'MONDAY'),
        (TUE, 'TUESDAY'),
        (WEN, 'WENSDAY'),
        (THU, 'THURSDAY'),
        (FRI, 'FRIDAY'),
        (SAT, 'SATURDAY'),
        (SUN, 'SUNDAY')
    )

    id = models.AutoField(primary_key=True)
    didaskalia_id = models.ForeignKey(
        Didaskalia, on_delete=models.SET_NULL, null=True)
    day = models.CharField(max_length=3, choices=DAYS_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    location = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        ordering = ['-date']


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    didaskalia_id = models.ForeignKey(
        Didaskalia, on_delete=models.SET_NULL, null=True)
    content = models.TextField(help_text='Announcement to make')
    date = models.DateField(default=datetime.now)

    class Meta:
        ordering = ['-date']


class Secr_Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(help_text='Announcement to make')
    photo = models.ImageField(
        upload_to='images/secr_announcements', null=True, blank=True)
    date = models.DateField(default=datetime.now)

    class Meta:
        ordering = ['-date']


class Drastiriotita(models.Model):

    ERGASIA = 'ERGASIA'
    PROODOS = 'PROODOS'
    ERGASTIRIO = 'ERGASTIRIO'
    EKSETASTIKI = 'EKSTETASTIKI'

    DRASTIRIOTITES_CHOICES = (
        (ERGASIA, 'ERGASIA'),
        (PROODOS, 'PROODOS'),
        (ERGASTIRIO, 'ERGASTIRIO'),
        (EKSETASTIKI, 'EKSTETASTIKI')
    )

    id = models.AutoField(primary_key=True)
    didaskalia = models.ForeignKey(
        Didaskalia, on_delete=models.CASCADE)
    sintelestis = models.FloatField()
    due_date = models.DateTimeField()
    tipos = models.CharField(max_length=25, choices=DRASTIRIOTITES_CHOICES)
    title = models.CharField(max_length=45)
    perigrafi = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return f'{self.didaskalia.get_name()}: {self.tipos} {self.id}'

    def due_date_not_passed(self):
        if(self.due_date > datetime.now(timezone.utc)):
            return True
        return False

    def time_left(self):
        time = self.due_date - datetime.now(timezone.utc)
        time = str(time).split(".")[0]
        return f'{time} Hours'

    def people_to_deliver(self):
        return SimmetoxiDrastiriotita.objects.filter(
            drastiriotita=self).count()

    def people_delivered(self):
        return SimmetoxiDrastiriotita.objects.filter(
            drastiriotita=self, delivered=True).count()


class Professor(models.Model):
    PROFESSOR = 'PROF'
    EPIKOUROS = 'EPIK'
    ANAPLHRWTHS = 'ANAPL'
    OMOTIMOS = 'OMOT'
    EPITIMOS = 'EPIT'

    PROFESSOR_TITLE = (
        (PROFESSOR, 'Καθηγητής'),
        (EPIKOUROS, 'Eπίκουρος Καθηγητής'),
        (ANAPLHRWTHS, 'Αναπληρωτής Καθηγητής'),
        (OMOTIMOS, 'Ομότιμος Καθηγητής'),
        (EPITIMOS, 'Επίτιμος Καθηγητής')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=5, choices=PROFESSOR_TITLE, default=PROFESSOR)
    tomeas = models.CharField(max_length=100)
    didaskalia = models.ManyToManyField(Didaskalia, null=True, blank=True)

    # Metadata
    class Meta:
        ordering = ['title']

    def didaskei(self, didaskalia_id):
        didaskei = self.didaskalia.all().values_list('id', flat=True)
        if(didaskalia_id in didaskei):
            return True
        return False

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def name(self):
        prof = Profile.objects.get(professor=self.id)
        return prof.name()


class Student(models.Model):

    HMTY = 'HMTY'
    CEID = 'CEID'

    DEPT_CHOICES = (
        (HMTY, 'HMTY'),
        (CEID, 'CEID')
    )

    HMTY_Bachelor = 'HMTY_Bachelor'
    HMTY_Masters = 'HMTY_Masters'

    PROGRAMMA_SPOUDWN_CHOICES = (
        (HMTY_Bachelor, 'HMTY_Bachelor'),
        (HMTY_Masters, 'HMTY_Masters')
    )

    am = models.AutoField(primary_key=True)
    age = models.IntegerField()
    date_eisagwghs = models.DateField(auto_now_add=True)
    department = models.CharField(max_length=20, choices=DEPT_CHOICES)
    programma_spoudwn = models.CharField(
        max_length=20, choices=PROGRAMMA_SPOUDWN_CHOICES)
    tomeas = models.CharField(max_length=100, null=True, blank=True)
    didaskalia = models.ManyToManyField(Didaskalia, through="Dilosi")
    drastiriotita = models.ManyToManyField(
        Drastiriotita, through="SimmetoxiDrastiriotita")
    thesis = models.ForeignKey(
        'Thesis', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-am']

    def __str__(self):
        return f'{self.am} - {self.name()}'

    def parakolouthei(self, didaskalia_id):
        if(Dilosi.objects.filter(student=self, didaskalia=didaskalia_id)):
            return True
        return False

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.am)])

    def name(self):
        profile = Profile.objects.filter(student=self)
        if(profile):
            return profile[0].name()
        return None


class Dilosi(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    didaskalia = models.ForeignKey(Didaskalia, on_delete=models.CASCADE)
    telikos_vathmos = models.FloatField(max_length=4, null=True, blank=True)

    def __str__(self):
        return f'{self.student.name()} - {self.didaskalia.get_name()}'


class Certificate(models.Model):
    cert_id = models.AutoField(primary_key=True)
    cert_type = models.CharField(max_length=50)
    date_requested = models.DateField(auto_now_add=True)
    available = models.BooleanField()
    received = models.BooleanField()
    student_am = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-cert_id']

    def __str__(self):
        return f'{self.cert_id}'

    # Returns the url to access a particular instance of the model.

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.cert_id)])


class Thesis(models.Model):
    thesis_id = models.AutoField(primary_key=True)
    subject = models.TextField()
    grade = models.FloatField(null=True, blank=True)
    date_anathesis = models.DateField(auto_now_add=True)
    date_paradosis = models.DateField(null=True)

    class Meta:
        ordering = ['-thesis_id']

    def __str__(self):
        return f'{self.thesis_id}'

    # Returns the url to access a particular instance of the model.

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.thesis_id)])


class SimmetoxiDrastiriotita(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.SET_NULL, null=True)
    drastiriotita = models.ForeignKey(
        Drastiriotita, on_delete=models.SET_NULL, null=True)
    grade = models.FloatField(null=True, blank=True)
    file = models.FileField(upload_to='files', null=True, blank=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student}: {self.drastiriotita}'

    def get_grade(self):
        return '-' if self.grade == None else self.grade


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fathername = models.CharField(max_length=20)
    photo = models.ImageField(
        upload_to='images/avatars', null=True, blank=True)
    grammateia = models.BooleanField(default=False)
    student = models.ForeignKey(
        Student, on_delete=models.SET_NULL, null=True, blank=True)
    professor = models.ForeignKey(
        Professor, on_delete=models.SET_NULL, null=True, blank=True)

    def get_my_courses(self):
        if(self.is_student()):
            return self.student.didaskalia.all()
        elif(self.is_professor()):
            return self.professor.didaskalia.all()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def etos(self):
        if(self.is_student()):
            return abs(datetime.now().year - self.student.date_eisagwghs.year) + 1

    def idiotita(self):
        if (self.is_student()):
            return u'Φοιτητής'
        elif (self.is_professor()):
            return self.professor.get_title_display()
        elif (self.is_grammateia()):
            return u'Γραμματεία'
            
    def get_am(self):
        return self.student.am

    def is_student(self):
        if (self.student is not None):
            return True
        return False

    def is_professor(self):
        if (self.professor is not None):
            return True
        return False

    def is_grammateia(self):
        return self.grammateia

    def __str__(self):
        return f'{self.id} -  {self.user.first_name} {self.user.last_name}'

    def name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def image_url(self):
        """
        Returns the URL of the image associated with this Object.
        If an image hasn't been uploaded yet, it returns a stock image

        :returns: str -- the image url

        """
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return '/static/images/avatar2.png'
