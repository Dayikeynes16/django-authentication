from django.urls import path
from . import views

urlpatterns = [
    path('',  views.DS, name='DS'),
]
