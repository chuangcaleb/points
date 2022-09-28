from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<str:group>', views.group_view, name='group'),
    path('group/<str:group>/history', views.history_view, name='history'),
]
