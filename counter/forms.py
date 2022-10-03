from django.forms import ModelForm
from .models import Event, Group
# from django.utils.translation import gettext_lazy as _


class EventForm(ModelForm):

    class Meta:
        model = Event

        fields = ['name']


class GroupForm(ModelForm):
    class Meta:
        model = Group

        fields = ['name']
