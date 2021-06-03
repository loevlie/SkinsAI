from django.urls import re_path,path, include, re_path
from . import views
from django.conf.urls import url

app_name = 'Portfolio'

urlpatterns = [
    path('success/',views.successView,name='success'),
    path('', views.PostList.as_view(), name='home'),
    #path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    #re_path(r'^Blog/$', views.blog, name='Blog'),
]