from django.urls import path
from django.views.generic import TemplateView
"""
from .views import (
    home_page, 
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    post_share,
    post_comment,
    )
"""
    
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='project_HomePage'),
]