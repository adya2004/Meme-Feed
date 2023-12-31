from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from . import meme_temp as mt
from django.http import JsonResponse

#function based view for home page
def home(request):
    context = {
        'posts': post.objects.all()
    }
    return render(request, 'blog/home.html', context)
    #this will return http response in background as required

#function based view for about page
def about(request):
    return render(request, 'blog/about.html', {'title' : 'About'})

#class based view for displaying posts
class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

#class based view for displaying individual post in detail
class PostDetailView(DetailView):
    model = post

#class based view for creating posts
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

#class based view for updating posts    
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
        
#class based view for deleting posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#class based view for displaying  user posts    
class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')


#this feature is incomplete and will be updated in future
# def like_post(request, pk):
#     post = get_object_or_404(post, pk=pk)
#     if request.user not in post.like_set.all():
#         Like.objects.create(user=request.user, post=post)
#         post.like_count += 1
#         post.save()
#         liked = True
#     else:
#         Like.objects.filter(user=request.user, post=post).delete()
#         post.like_count -= 1
#         post.save()
#         liked = False
#     return JsonResponse({'liked': liked, 'like_count': post.like_count})


#class based view for displaying all meme templates
class Meme_templates(ListView):
    template_name = 'blog/meme_templates.html'
    context_object_name = 'meme_templates'
    paginate_by = 10
    def get_queryset(self):
        # Create a list of custom objects or dictionaries
        custom_object_list = mt.get_templates()
        return custom_object_list