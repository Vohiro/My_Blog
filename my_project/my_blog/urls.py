from django.urls import path
from .views import (
    home_page, 
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    post_share
    )

urlpatterns = [
    path('', home_page, name='home_page'),
    # Post views
    path('blog/post_list/', PostListView.as_view(), name='post_list'),
    path('blog/post_detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('blog/<slug:slug>/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('blog/post_new/', PostCreateView.as_view(), name='post_new'),
    path('blog/post_detail/<int:pk>/post_edit/', PostUpdateView.as_view(), name='post_edit'),
    path('blog/post_detail/<int:pk>/post_delete/', PostDeleteView.as_view(), name='post_delete'),
    path('blog/post_detail/<int:pk>/post_share/', post_share, name='post_share'),
]