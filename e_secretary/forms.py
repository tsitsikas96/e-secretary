from django import forms
from .models import Profile


class ChangeAvatarForm(forms.Form):

    photo = forms.ImageField(
        required=True,
        help_text='Choose an image to replace your avatar',
        label='',
    )

    fields = ['photo']
