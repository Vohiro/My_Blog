from django.urls import path
from .views import home_page, PostListView, PostDetailView

urlpatterns = [
    path('', home_page, name='home_page'),
    path('blog/post_list/', PostListView.as_view(), name='post_list'),
    path('blog/post_detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]