from django.shortcuts import get_object_or_404, render

from .models import Group

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
    # First time loading the page
    if request.method == "POST":

        group_obj = get_object_or_404(Group, pk=group)

        if 'reset' in request.POST:

            setattr(group_obj, 'points', 0)
            group_obj.save(update_fields=['points'])

        else:

            if request.POST["offset"]:
                offset = int(request.POST["offset"])
            else:
                return render(request, "group.html", {
                    'group': get_object_or_404(Group, pk=group)
                })

            current_points = getattr(group_obj, 'points')

            setattr(group_obj, 'points', current_points+offset)
            group_obj.save(update_fields=['points'])

        return render(request, "group.html", {
            'group': get_object_or_404(Group, pk=group)
        })

    else:

        return render(request, "group.html", {
            'group': get_object_or_404(Group, pk=group)
        })
