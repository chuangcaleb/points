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
        exclude = ['name', 'slug']
        labels = {
            'bg_url': 'Background Image URL',
            'font': 'Font Family',
            'font_link': 'Google Font URL',
            'color': "Text Color",
            'default_card_color': "Default Card Colour",
            'heading_size': "Heading Font Size",
            'points_size': "Points Font Size",
        }
