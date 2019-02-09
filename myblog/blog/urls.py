from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='feed'),
    path('about/', views.about, name='about'),
    re_path(r'^post/(?P<slug>[-\w]+)/$', views.detail),
]
