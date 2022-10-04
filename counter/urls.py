from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/<str:event>',
         views.event_json_response, name='event_json'),
    path('<str:event>', views.event_view, name='event'),
    path('<str:event>/<str:group>', views.group_view, name='group'),
    path('<str:event>/<str:group>/history',
         views.history_view, name='history'),
]
