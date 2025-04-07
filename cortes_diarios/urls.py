from django.urls import path
from . import views

urlpatterns = [
    path('',  views.DS, name='DS'),
    path('cortes/', views.CortesDiariosView.as_view(), name='cortes'),
    path('historial/', views.historial.as_view())
]
