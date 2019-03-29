from django.contrib import admin

# Register your models here.

from e_secretary.models import Course, Didaskalia, Orologio, Announcement, Grammateia, Drastiriotita, Professor, Student, Dilosi, Certificate, Thesis, SimmetoxiDrastiriotita, Event, Secr_Announcement


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'tomeas', 'ects', 'ipoxrewtiko')


admin.site.register(Event)
admin.site.register(Didaskalia)
admin.site.register(Orologio)
admin.site.register(Announcement)
admin.site.register(Grammateia)
admin.site.register(Drastiriotita)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Dilosi)
admin.site.register(Certificate)
admin.site.register(Thesis)
admin.site.register(SimmetoxiDrastiriotita)
admin.site.register(Secr_Announcement)
