from django.db import models
from django.urls import reverse
from datetime import datetime

# Create your models here.
# YOLO


class Course(models.Model):
    """A typical class defining a model, derived from the Model class."""
    # Fields
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, help_text='Course Name')
    tomeas = models.CharField(max_length=100, help_text='Tomeas Name')
    ects = models.IntegerField()
    programma_spoudwn = models.CharField(
        max_length=200, help_text='Programma Spoudwn')
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
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    akad_etos = models.IntegerField(choices=YEAR_CHOICES,
                                    default=datetime.now().year)
    eksamino = models.CharField(max_length=9, choices=SEMESTER_CHOICES)

    # Metadata
    class Meta:
        ordering = ['akad_etos']

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'{self.course_id}'

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Course."""
        return reverse('model-detail-view', args=[str(self.id)])


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
    time = models.TimeField()


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
    photo = models.ImageField(
        upload_to='images/announcements', null=True, blank=True)
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


class Grammateia(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50, help_text='First Name')
    lname = models.CharField(max_length=50, help_text='Last Name')
    email = models.EmailField()

    def __str__(self):
        return f'{self.fname} {self.lname}'


class Drastiriotita(models.Model):
    id = models.AutoField(primary_key=True)
    didaskalia_id = models.ForeignKey(
        Didaskalia, on_delete=models.SET_NULL, null=True)
    sintelestis = models.FloatField()
    date = models.DateTimeField()
    tipos = models.CharField(max_length=45)

    def __str__(self):
        return f'{self.didaskalia_id}: {self.tipos}'


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
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    title = models.CharField(
        max_length=5, choices=PROFESSOR_TITLE, default=PROFESSOR)
    email = models.EmailField()
    tomeas = models.CharField(max_length=100)
    didaskalia = models.ManyToManyField(Didaskalia)

    # Metadata
    class Meta:
        ordering = ['lname']

    def __str__(self):
        return f'{self.fname} {self.lname}'

    # Returns the url to access a particular instance of the model.

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])


class Student(models.Model):
    am = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    fathername = models.CharField(max_length=20)
    age = models.IntegerField()
    date_eisagwghs = models.DateField(auto_now_add=True)
    department = models.CharField(max_length=100)
    programma_spoudwn = models.CharField(max_length=10)
    tomeas = models.CharField(max_length=100, null=True, blank=True)
    didaskalia = models.ManyToManyField(Didaskalia, through="Dilosi")
    drastiriotita = models.ManyToManyField(
        Drastiriotita, through="SimmetoxiDrastiriotita")
    email = models.EmailField()

    class Meta:
        ordering = ['-am']

    def __str__(self):
        return f'{self.fname} {self.lname} {self.am}'

    # Returns the url to access a particular instance of the model.

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.am)])


class Dilosi(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    didaskalies = models.ForeignKey(Didaskalia, on_delete=models.CASCADE)
    telikos_vathmos = models.FloatField(max_length=5)


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
    student_am = models.ForeignKey(Student, on_delete=models.CASCADE)

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

    def __str__(self):
        return f'{self.student}: {self.drastiriotita}'
