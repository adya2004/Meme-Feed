from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from . import meme_temp as mt

def home(request):
    context = {
        'posts': post.objects.all()
    }
    return render(request, 'blog/home.html', context)
    #this will return http response in background as required

def about(request):
    return render(request, 'blog/about.html', {'title' : 'About'})

class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

class PostDetailView(DetailView):
    model = post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'template_id', 'top_text', 'bottom_text',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        template_id = form.cleaned_data['template_id'] 
        top_text = form.cleaned_data['top_text']
        bottom_text = form.cleaned_data['bottom_text']
        meme_url = mt.generate_meme(template_id, top_text, bottom_text)
        if meme_url is not None:
            form.instance.meme = meme_url
            return super().form_valid(form)
        else:
            # Handle the case where meme generation failed
            form.add_error(None, "Meme generation failed. Please try again.")
            return self.form_invalid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'template_id', 'top_text', 'bottom_text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        template_id = form.cleaned_data['template_id'] 
        top_text = form.cleaned_data['top_text']
        bottom_text = form.cleaned_data['bottom_text']
        meme_url = mt.generate_meme(template_id, top_text, bottom_text)
        if meme_url is not None:
            form.instance.meme = meme_url
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 
        
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')