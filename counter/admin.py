from django.contrib import admin

from .models import Event, Group, PointsHistory

# Register your models here.


class EventAdmin(admin.ModelAdmin):
    exclude = ['slug']


admin.site.register(Event, EventAdmin)


class GroupAdmin(admin.ModelAdmin):
    exclude = ['slug']


admin.site.register(Group, GroupAdmin)

admin.site.register(PointsHistory)
