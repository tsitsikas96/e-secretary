from django.db import models
from django.urls import reverse

# Create your models here.

class Professor(models.Model):

    PROFESSOR = 'PROF'
    EPIKOUROS = 'EPIK'
    ANAPLHRWTHS = 'ANAPL'
    OMOTIMOS = 'OMOT'
    EPITIMOS = 'EPIT'

    PROFESSOR_TITLE = (
        (PROFESSOR,'Καθηγητής'),
        (EPIKOUROS, 'Eπίκουρος Καθηγητής'),
        (ANAPLHRWTHS, 'Αναπληρωτής Καθηγητής'),
        (OMOTIMOS, 'Ομότιμος Καθηγητής'),
        (EPITIMOS, 'Επίτιμος Καθηγητής')
    )

    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=20)
    sname = models.CharField(max_length=20)
    title = models.CharField(max_length=5,choices=PROFESSOR_TITLE,default=PROFESSOR)
    mail = models.EmailField()
    tomeas = models.CharField(max_length=100)
    didaskalia = models.ManyToManyField(Didaskalia)

    # Metadata
    class Meta:
        ordering = ['-surname']

    def __str__(self):
        return self.id

    # Returns the url to access a particular instance of the model.

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

class Student(models.Model):

    am = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=20)
    sname = models.CharField(max_length=20)
    fathername = models.CharField(max_length=20)
    age = models.IntegerField(max_length=2)
    date_eisagwghs = models.DateField(auto_now_add=True)
    department = models.CharField(max_length=100)
    programma_spoudwn = models.CharField(max_length=10)
    tomeas = models.CharField(max_length=100,null=True)
    didaskalia = models.ManyToManyField(Didaskalia,through="Dilosi")
    drastiriotita = models.ManyToManyField(Drastiriotita,through="SimmetoxiDrastiriotita")


    class Meta:
        ordering = ['-am']

    def __str__(self):
        return self.am

    # Returns the url to access a particular instance of the model.

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.am)])

class Dhlwsh(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    didaskalies = models.ForeignKey(Didaskalia,on_delete=models.CASCADE)
    telikos_vathmos = models.FloatField(max_length=5)

class Certificate(models.Model):

    cert_id = models.AutoField(primary_key=True)
    cert_type = models.CharField(max_length=50)
    date_requested = models.DateField(auto_now_add=True)
    available = models.BooleanField()
    received = models.BooleanField()
    student_am = models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        ordering = ['-cert_id']

    def __str__(self):
        return self.cert_id

    # Returns the url to access a particular instance of the model.

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.cert_id)])

class Thesis(models.Model):

    thesis_id = models.AutoField(primary_key=True)
    subject = models.TextField()
    vathmos = models.FloatField(max_length=5)
    date_anathesis = models.DateField(auto_now_add=True)
    date_paradosis = models.DateField(null=True)
    student_am = models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        ordering = ['-thesis_id']

    def __str__(self):
        return self.thesis_id

    # Returns the url to access a particular instance of the model.

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.thesis_id)])

