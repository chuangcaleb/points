from django.shortcuts import render
from .models import PointsRecord

# Create your views here.


def index(request):
    return render(request, "index.html", {
        'pointsrecords': PointsRecord.objects.all()
    })
