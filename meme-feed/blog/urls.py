from django.urls import path
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView,
    PostDeleteView, 
    UserPostListView, 
    Meme_templates
)

# Define URL patterns
urlpatterns = [
    # Home page to display a list of posts
    path('', PostListView.as_view(), name="blog-home"),

    # About page
    path('about/', views.about, name='blog-about'),

    # Display details of a specific post using its primary key
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),

    # Create a new post
    path('post/new/', PostCreateView.as_view(), name='post-create'),

    # Update an existing post based on its primary key
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),

    # Delete an existing post based on its primary key
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),

    # Display a list of posts by a specific user using their username
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    # Display meme templates
    path('templates/', Meme_templates.as_view(), name='meme-templates')
]
