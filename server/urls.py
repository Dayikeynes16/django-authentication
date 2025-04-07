"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='access_token'),  # Endpoint para obtener tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('', views.index),
    path('users/', views.UserIformation.as_view(), name='users'),
    path('admin/', admin.site.urls),
    path('cortes/', include('cortes_diarios.urls')),
    path('todo/', include('to_do.urls')), 
    path('roles/', views.SaveRolesView.as_view(), name='save-roles'),
    path('register/', views.SaveUserView.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('update_user/<int:pk>/', views.UpdateUser.as_view(), name='update_user')
]
