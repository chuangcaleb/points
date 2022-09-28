from django.contrib import admin

from .models import Group, PointsHistory

# Register your models here.

admin.site.register(Group)
# admin.site.register(PointsRecord)
admin.site.register(PointsHistory)
