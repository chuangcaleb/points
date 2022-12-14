import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse

from .forms import (NewEventForm, NewGroupForm, UpdateCssForm,
                    UpdateGroupCssForm)
from .models import Event, Group, PointsHistory

# Create your views here.


def index(request):

    if request.method == "POST":

        form = NewEventForm(request.POST)

        if form.is_valid():

            form.save()

        return render(request, "index.html", {
            'events': Event.objects.all(),
            'form': form
        })

    else:

        return render(request, "index.html", {
            'events': Event.objects.all(),
            'form': NewEventForm()
        })


def event_view(request, event):

    event_obj = get_object_or_404(Event, slug=event)

    def get_groups():
        # event.slug = event slug
        return Group.objects.filter(event__slug=event)

    def _default_render():

        return render(request, "event.html", {
            'event': get_object_or_404(Event, slug=event),
            'name_form': NewGroupForm(),
            'css_form': UpdateCssForm(instance=event_obj),
            'groups': get_groups()
        })

    if request.method == "POST":

        # delete event, return to index
        if 'delete_event' in request.POST:

            event_obj.delete()  # This delete cascades to delete relevant groups

            return redirect('index')

        if 'reset' in request.POST:

            groups_obj = get_groups()

            # Update all groups to have 0 points
            groups_obj.update(points=0)

            # Delete all relevant history
            group_histories = PointsHistory.objects.filter(
                group__in=groups_obj)
            group_histories.delete()

            return _default_render()

        if 'name' in request.POST:

            name_form = NewGroupForm(request.POST)

            if name_form.is_valid():

                # new_group = name_form.save(commit=False)
                name_form.instance.points = 0
                # new_group.points = 0
                name_form.instance.event = get_object_or_404(
                    Event, slug=event)

                # Create entry in Group model
                # new_group.save()
                name_form.save()

            return render(request, "event.html", {
                'event': get_object_or_404(Event, slug=event),
                'name_form': name_form,
                'css_form': UpdateCssForm(instance=event_obj),
                'groups': get_groups()
            })

        # Else, all other requests are CSS edits
        css_form = UpdateCssForm(data=request.POST, instance=event_obj)

        if css_form.is_valid():
            css_form.save()

        return render(request, "event.html", {
            'event': get_object_or_404(Event, slug=event),
            'name_form': NewGroupForm(),
            'css_form': css_form,
            'groups': get_groups()
        })

    else:  # Render default for GET requests

        return _default_render()


def group_view(request, event, group):

    event_obj = get_object_or_404(Event, slug=event)
    group_obj = get_object_or_404(Group, event=event_obj, slug=group)

    if request.method == "POST":

        if 'delete_group' in request.POST:

            group_obj.delete()
            return redirect('event', event)

        if 'reset' in request.POST:

            setattr(group_obj, 'points', 0)
            group_obj.save(update_fields=['points'])

            group_histories = PointsHistory.objects.filter(
                group=group_obj)
            group_histories.delete()

        # If offset exists AND is not null
        if ('offset' in request.POST) and (
                request.POST["offset"] not in ('', 0)):

            # Offset points
            offset = int(request.POST["offset"])
            current_points = getattr(group_obj, 'points')

            setattr(group_obj, 'points', current_points+offset)
            group_obj.save(update_fields=['points'])

            # Log points to history
            history_obj = PointsHistory(
                group=group_obj,
                offset=offset,
            )
            history_obj.save()

        else:  # POST request to update css

            group_css_form = UpdateGroupCssForm(
                data=request.POST, instance=group_obj)
            if group_css_form.is_valid():
                group_css_form.save()

    # At any GET and at the end of POST, render
    return render(request, "group.html", {
        'event': event_obj,
        'group': group_obj,
        'css_form': UpdateGroupCssForm(instance=group_obj)
    })


def history_view(request, event, group):

    event_obj = get_object_or_404(Event, slug=event)
    group_obj = get_object_or_404(Group, event=event_obj, slug=group)

    history_records = PointsHistory.objects.values_list(
        'offset', flat=True
    ).filter(group=group_obj).reverse()
    history_table = [
        {
            'p': "green" if offset > 0 else "red",
            'o': offset,
            's': sum(history_records[0:i+1])
        }
        for i, offset in enumerate(history_records)
    ]

    return render(request, "history.html", {
        'event': event_obj,
        'group': group_obj,
        'history': list(history_table)
    })


def event_json_response(request, event):
    event_obj = Group.objects.filter(event__slug=event)
    event_dict = {i.slug: i.points for i in event_obj}
    event_json = json.dumps(event_dict)
    return HttpResponse(event_json, content_type='application/json')
