from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='feed'),
    path('about/', views.about, name='about'),
    re_path(r'^post/(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='post-detail'),
    path( 'post-create/', views.PostCreateView.as_view(), name='post-create'),
    re_path(r'^post/(?P<slug>[-\w]+)/update', views.PostUpdateView.as_view(), name='post-update'),
    re_path( r'^post/(?P<slug>[-\w]+)/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user-posts'),
]
