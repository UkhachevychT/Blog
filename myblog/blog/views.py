from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
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

from . import models
from .filters import PostFilter

class PostListView(ListView):
    model = models.Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    # filter_class = PostFilter
    paginate_by = 5


class UserPostListView(ListView):
    model = models.Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return models.Post.objects.filter(author=user)

class PostDetailView(DetailView):
    model = models.Post
    template_name = 'blog/post.html'

    def get_context_data(self, **kwargs):
        post = self.get_object()
        context = super().get_context_data(**kwargs)
        context['comments'] = models.Comment.objects.filter(post=post)
        return context

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
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = models.Comment
    fields = ['body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = models.Post.objects.get(slug=self.kwargs['slug'])

        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        return reverse('post-detail', args=(self.kwargs['slug'],))

def index(request):
    posts = models.Post.objects.all()
    post_filter = PostFilter(request.GET, queryset=posts)
    return render(request, 'blog/index.html', {
        'posts': posts,
        'filter': post_filter,
    })

def about(request):
    return render(request, 'blog/about.html')

def detail(request, slug):
    post = get_object_or_404(models.Post, slug=slug)

    return render(request, 'blog/post.html', {
        'post': post,
    })