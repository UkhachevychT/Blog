from django.shortcuts import render, get_object_or_404

from. import models

def index(request):
    posts = models.Post.objects.all()
    return render(request, 'blog/index.html', {
        'posts': posts,
    })

def about(request):
    return render(request, 'blog/about.html')

def detail(request, slug):
    post = get_object_or_404(models.Post, slug=slug)

    return render(request, 'blog/post.html', {
        'post': post,
    })