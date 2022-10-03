from django.forms import ModelForm
from .models import Event, Group
# from django.utils.translation import gettext_lazy as _


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

        fields = ['css']
