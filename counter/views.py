from .models import PointsRecord
from django.shortcuts import get_object_or_404, render

# Create your views here.


def index(request):

    if request.method == "POST":

        record_obj = PointsRecord.objects.all()

        if 'reset' in request.POST:

            # setattr(record_obj, 'points', 0)
            # record_obj.save(update_fields=['points'])
            record_obj.update(points=0)

    return render(request, "index.html", {
        'pointsrecords': PointsRecord.objects.all()
    })


def group_view(request, group):
    # First time loading the page
    if request.method == "POST":

        record_obj = get_object_or_404(PointsRecord, pk=group)

        if 'reset' in request.POST:

            setattr(record_obj, 'points', 0)
            record_obj.save(update_fields=['points'])

        else:

            current_points = getattr(record_obj, 'points')
            offset = int(request.POST["offset"])

            setattr(record_obj, 'points', current_points+offset)
            record_obj.save(update_fields=['points'])

        return render(request, "group.html", {
            'record': get_object_or_404(PointsRecord, pk=group)
        })

    else:

        return render(request, "group.html", {
            'record': get_object_or_404(PointsRecord, pk=group)
        })
