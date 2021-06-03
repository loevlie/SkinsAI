"""LoevlieDL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls import url
from Portfolio import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$',views.index,name='index'),
    re_path(r'^timeline/$',views.timeline,name='timeline'),
    re_path(r'^portfolio/$',views.portfolio,name='portfolio'),
    #re_path(r'^Blog/$',views.blog,name='Blog'),
    re_path(r'^Blog/$', views.blog.as_view(), name='Blog'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('', include('Portfolio.urls')), # new
]
