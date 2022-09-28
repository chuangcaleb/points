from .models import PointsRecord
from django.shortcuts import get_object_or_404, render

# Create your views here.


def index(request):
    return render(request, "index.html", {
        'pointsrecords': PointsRecord.objects.all()
    })


def group_view(request, group):
    return render(request, "group.html", {
        'group': get_object_or_404(PointsRecord, pk=group)

    })
