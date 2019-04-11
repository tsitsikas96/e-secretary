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
        attrs = {'class': 'table table-hover table-bordered','id':'table-didask'}
        template_name= 'django_tables2/bootstrap-responsive.html'

class DilosiTable(tables.Table):
    id = tables.Column(verbose_name="Κωδικός",orderable=False)
    name = tables.Column(verbose_name="Μάθημα",orderable=False)
    tomeas = tables.Column(verbose_name="Τομέας",orderable=False)
    ects = tables.Column(verbose_name="ECTS",orderable=False)

    class Meta:
        fields = ['id','name','tomeas','ects']
        attrs = {'class': 'table table-hover table-bordered','id':'table-dilosi'}
        template_name= 'django_tables2/bootstrap-responsive.html'