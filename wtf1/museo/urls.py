from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth import urls
app_name='museo'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.login, {'template_name':'login.html'},name='login'),
    path('logout/',auth_views.logout,{'template_name':'logged_out.html'},name='logout'),
    path('feed/',views.feed,name='feed'),
]