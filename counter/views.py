from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse

from .models import Group, PointsHistory

# Create your views here.


def index(request):

    if request.method == "POST":

        record_obj = Group.objects.all()

        if 'reset' in request.POST:

            # setattr(record_obj, 'points', 0)
            # record_obj.save(update_fields=['points'])
            record_obj.update(points=0)

    return render(request, "index.html", {
        'groups': Group.objects.all()
    })


def group_view(request, group):

    def _render(request, group):
        return render(request, "group.html", {
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


def history_view(request, group):

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
        'group': get_object_or_404(Group, pk=group),
        'history': list(history_table)
    })
