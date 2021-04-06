from django.urls import path, include, re_path
from . import views
from django.conf.urls import url

app_name = 'Portfolio'

urlpatterns = [
    path('success/',views.successView,name='success'),
]