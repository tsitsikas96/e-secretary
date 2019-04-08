from django import forms
from .models import Announcement
from django.contrib.admin import widgets


class ChangeAvatarForm(forms.Form):

    photo = forms.ImageField(
        required=False,
        help_text='Choose an image to replace your avatar',
    )

    delete_photo = forms.BooleanField(
        required=False, help_text='Delete avatar')

    fields = ['photo', 'delete_photo']

    def clean(self):
        cleaned_data = super(ChangeAvatarForm, self).clean()

        photo = cleaned_data.get("photo")
        delete_photo = cleaned_data.get("delete_photo")

        if not photo and not delete_photo:  # both were entered
            raise forms.ValidationError(
                "You must delete the avatar or upload an image.")

        return cleaned_data


class FileUploadForm(forms.Form):
    file = forms.FileField(
        required=False,
    )

    fields = ['file']


class GradeUploadForm(forms.Form):
    grade = forms.FloatField(required=True)
    student_id = forms.IntegerField(required=True)

    fields = ['grade', 'student_id']


class NewErgasiaForm(forms.Form):

    DRASTIRIOTITES_CHOICES = ('ERGASIA', 'PROODOS',
                              'ERGASTIRIO', 'EKSTETASTIKI')

    sintelestis = forms.FloatField()
    due_date = forms.DateField()
    tipos = forms.CharField(max_length=45)
    title = forms.CharField(max_length=45)
    perigrafi = forms.CharField(max_length=400, widget=forms.Textarea)
    file = forms.FileField(required=False)

    fields = ['sintelestis', 'due_date',
              'tipos', 'title', 'perigrafi', 'file']

    def clean(self):
        # Then call the clean() method of the super  class
        cleaned_data = super(NewErgasiaForm, self).clean()
        print(cleaned_data)
        # ... do some cross-fields validation for the subclass
        if not cleaned_data['tipos'] in self.DRASTIRIOTITES_CHOICES:
            raise forms.ValidationError(
                "Tipos must be one of ('ERGASIA', 'PROODOS', 'ERGASTIRIO', 'EKSTETASTIKI')")
        # Finally, return the cleaned_data
        return cleaned_data


class NewAnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ['content']
