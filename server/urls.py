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
from django.urls import path, re_path
from . import views
# from .views import SaveRolesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('roles/', views.SaveRolesView.as_view(), name='save-roles'),
    path('register/', views.SaveUserView.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('update_user/<int:pk>/', views.UpdateUser.as_view(), name='update_user'),
    # path('profiles/', views.SaveUserProfileView.as_view(), name='save-profiles'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    # re_path('register', views.register),
    # re_path('register', views.register),
    # re_path('login', views.login),
    # re_path('profile', views.profile),
    # # re_path('update_user', views.update_user),
    # path('roles/', SaveRolesView.as_view(), name='save-roles'),


]
