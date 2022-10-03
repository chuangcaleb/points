from django.forms import ModelForm
from .models import Event, Group


class NewEventForm(ModelForm):

    class Meta:
        model = Event

        fields = ['name']


class NewGroupForm(ModelForm):
    class Meta:
        model = Group

        fields = ['name']


class UpdateCssForm(ModelForm):
    class Meta:
        model = Event
        fields = ['bg_url']
        labels = {
            'bg_url': 'Background Image URL',
        }
