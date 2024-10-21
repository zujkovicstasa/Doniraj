from django.forms import ModelForm
from django import forms
from .models import *
#Autor: Stasa Zujkovic
class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Unesite poruku ...', 'class': 'form-control', 'maxlength': '500', 'autofocus': True}),
        }
