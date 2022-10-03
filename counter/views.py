from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, redirect
from django.urls import reverse

from counter.forms import EventForm

from .models import Event, Group, PointsHistory

# Create your views here.


def index(request):

    if request.method == "POST":

        record_obj = Group.objects.all()
        form = EventForm(request.POST)

        if form.is_valid():

            # Create entry in User model
            event = form.save()

        return render(request, "index.html", {
            'events': Event.objects.all(),
            'form': form
        })

    else:

        return render(request, "index.html", {
            'events': Event.objects.all(),
            'form': EventForm()
        })


def event_view(request, event):

    groups_obj = Group.objects.filter(
        event__slug=event)  # event.slug = event slug

    if request.method == "POST":

        if 'delete' in request.POST:
            # delete event, return to index
            event = get_object_or_404(Event, slug=event)
            event.delete()  # This delete cascades to delete relevant groups

            return redirect('index')

        if 'reset' in request.POST:

            # Update all groups to have 0 points
            groups_obj.update(points=0)

            # Delete all relevant history
            group_histories = PointsHistory.objects.all()
            group_histories.delete()

    return render(request, "event.html", {
        'event': get_object_or_404(Event, slug=event),
        'groups': groups_obj
    })


def group_view(request, event, group):

    def _render(request, group):
        return render(request, "group.html", {
            'event': get_object_or_404(Event, slug=event),
            'group': get_object_or_404(Group, pk=group)
        })

    if request.method == "POST":

        group_obj = get_object_or_404(Group, pk=group)

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
    print(history_table)

    return render(request, "history.html", {
        'event': get_object_or_404(Event, slug=event),
        'group': get_object_or_404(Group, pk=group),
        'history': list(history_table)
    })
