import django_tables2 as tables
from e_secretary.models import *

class DidaskaliesTable(tables.Table):

    id = tables.Column(verbose_name="Κωδικός",orderable=False)
    name = tables.Column(verbose_name="Μάθημα",orderable=False)
    tomeas = tables.Column(verbose_name="Τομέας",orderable=False)
    ects = tables.Column(verbose_name="ECTS",orderable=False)
    programma_spoudwn = tables.Column(verbose_name="Πρόγραμμα", orderable=False)
    ipoxrewtiko = tables.BooleanColumn(verbose_name="Υποχρεωτικό",orderable=False)

    class Meta:
        attrs = {'class': 'table table-hover table-bordered table-striped','id':'table-didask'}
        template_name = 'django_tables2/bootstrap-responsive.html'

class DilosiTable(tables.Table):
    id = tables.Column(verbose_name="Κωδικός",orderable=False)
    name = tables.Column(verbose_name="Μάθημα",orderable=False)
    tomeas = tables.Column(verbose_name="Τομέας",orderable=False)
    ects = tables.Column(verbose_name="ECTS",orderable=False)

    class Meta:
        fields = ['id','name','tomeas','ects']
        attrs = {'class': 'table table-hover table-bordered table-striped','id':'table-dilosi'}
        template_name = 'django_tables2/bootstrap-responsive.html'

class VathmologiesProfTable(tables.Table):

    id = tables.Column(verbose_name="ΑΜ",orderable=False)
    ergasies = tables.Column(verbose_name="Εργασίες",orderable=False)
    proodos = tables.Column(verbose_name="Πρόοδοι",orderable=False)
    lab = tables.Column(verbose_name="Εργαστήριο",orderable=False)
    exams = tables.Column(verbose_name="Εξεταστική",orderable=False)
    telikos = tables.Column(verbose_name="Τελικός Βαθμός",orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-bordered table-vathmoi'}
        template_name = 'django_tables2/bootstrap-responsive.html'

class VathmologiesStudTable(tables.Table):
    name = tables.Column(verbose_name="Μάθημα",orderable=False)
    akad_etos = tables.Column(verbose_name="Έτος",orderable=False)
    telikos_vathmos = tables.Column(verbose_name="Τελικός Βαθμός",orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-bordered table-vathmoi'}
        template_name = 'django_tables2/bootstrap-responsive.html'

class CertificatesTable(tables.Table):
    cert_type = tables.Column(verbose_name='ΤΥΠΟΣ',orderable=False)
    copies = tables.Column(verbose_name='ΑΝΤΙΤΥΠΑ',orderable=False)
    date_requested = tables.DateColumn(verbose_name='ΗΜΕΡΟΜΗΝΙΑ',orderable=False)
    available= tables.BooleanColumn(verbose_name='ΔΙΑΘΕΣΙΜΟ',orderable=False)
    received = tables.BooleanColumn(verbose_name='ΠΑΡΑΔΟΘΗΚΕ',orderable=False)
    class Meta:
        model = Certificate
        fields = {'cert_type','copies','date_requested','available','received'}
        sequence = ('cert_type','copies','date_requested','available','received')
        attrs = {'class': 'table table-striped table-certs'}
        template_name = 'django_tables2/bootstrap-responsive.html'     