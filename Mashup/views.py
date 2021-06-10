from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'mashup/index.html', context)

class Feed(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'mashup/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class UserPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'mashup/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(publisher=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_url ='/'
    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.publisher:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.publisher:
            return True
        return False

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs.get("pk"))
        form.instance.publisher = self.request.user
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.publisher:
            return True
        return False

    def get_success_url(self):
           pk = self.kwargs["pk"]
           return reverse("post-detail", kwargs={"pk": pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.publisher:
            return True
        return False

    def get_success_url(self):
           pk = self.kwargs["pk"]
           return reverse("post-detail", kwargs={"pk": pk})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'mashup/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'mashup/profile.html', context)
