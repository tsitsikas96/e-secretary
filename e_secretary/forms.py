from django import forms
from .models import Profile


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
