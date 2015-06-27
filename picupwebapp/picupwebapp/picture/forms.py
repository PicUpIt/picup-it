from django import forms
from captcha.fields import CaptchaField
from models import Picture, Gallery
from django.forms import ModelForm

class UploadFileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = Picture
        fields = ['picture']

class GalleryLicenseForm(forms.ModelForm):
    class Meta:
	model = Gallery
	fields = ['license']