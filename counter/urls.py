from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:group>', views.group_view, name='group'),
    path('<str:group>/history', views.history_view, name='history'),
]
