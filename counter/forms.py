from django import forms
from .models import Event
# from django.utils.translation import gettext_lazy as _


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = ['name']
        # widgets = {
        #     'name': forms.TextInput(attrs={'placeholder': 'New Event'}),
        # }
