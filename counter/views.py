from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, redirect
from django.urls import reverse

from counter.forms import NewEventForm, NewGroupForm, UpdateCssForm

from .models import Event, Group, PointsHistory

# Create your views here.


def index(request):

    if request.method == "POST":

        form = NewEventForm(request.POST)

        if form.is_valid():

            # Create entry in User model
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

    def get_groups():
        # event.slug = event slug
        return Group.objects.filter(event__slug=event)

    if request.method == "POST":

        if 'delete_event' in request.POST:

            # delete event, return to index
            event_obj = get_object_or_404(Event, slug=event)
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

        if 'name' in request.POST:

            name_form = NewGroupForm(request.POST)

            if name_form.is_valid():

                group = name_form.save(commit=False)
                group.points = 0
                group.event_id = get_object_or_404(Event, slug=event)

                # Create entry in User model
                name_form.save()

            return render(request, "event.html", {
                'event': get_object_or_404(Event, slug=event),
                'name_form': name_form,
                'css_form': UpdateCssForm(),
                'groups': get_groups()
            })

        if 'css' in request.POST:

            event_obj = get_object_or_404(Event, slug=event)

            css_form = UpdateCssForm(request.POST, instance=event_obj)

            if css_form.is_valid():

                updated_obj = css_form.save(commit=False)
                updated_obj.points = 0
                # group.event_id = get_object_or_404(Event, slug=event)

                # Create entry in User model
                css_form.save()

            return render(request, "event.html", {
                'event': get_object_or_404(Event, slug=event),
                'name_form': NewGroupForm(),
                'css_form': css_form,
                'groups': get_groups()
            })

    return render(request, "event.html", {
        'event': get_object_or_404(Event, slug=event),
        'name_form': NewGroupForm(),
        'css_form': UpdateCssForm(),
        'groups': get_groups()
    })


def group_view(request, event, group):

    def _render(request, group):
        return render(request, "group.html", {
            'event': get_object_or_404(Event, slug=event),
            'group': get_object_or_404(Group, pk=group)
        })

    if request.method == "POST":

        group_obj = get_object_or_404(Group, pk=group)

        if 'delete_group' in request.POST:

            group_obj.delete()
            return redirect('event', event)

        if 'reset' in request.POST:

            setattr(group_obj, 'points', 0)
            group_obj.save(update_fields=['points'])

            group_histories = PointsHistory.objects.filter(
                group=group_obj)
            group_histories.delete()

        else:  # POST request to offset

            # Terminate if 0 or null offset
            if request.POST["offset"] in ('', 0):
                return _render(request, group)

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

    # At any GET and at the end of POST, render
    return _render(request, group)


def history_view(request, event, group):

    history_records = PointsHistory.objects.values_list(
        'offset', flat=True).filter(group=group).reverse()
    history_table = [
        {
            'p': "green" if offset > 0 else "red",
            'o': offset,
            's': sum(history_records[0:i+1])
        }
        for i, offset in enumerate(history_records)
    ]

    return render(request, "history.html", {
        'event': get_object_or_404(Event, slug=event),
        'group': get_object_or_404(Group, pk=group),
        'history': list(history_table)
    })
