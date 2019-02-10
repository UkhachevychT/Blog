from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from. import models

class PostListView(ListView):
    model = models.Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = models.Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = models.Post
    fields = ['title', 'body', 'img']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Post
    fields = ['title', 'body', 'img']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Post
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    


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