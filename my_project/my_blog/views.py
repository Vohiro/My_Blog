from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

def home_page(request):
    return render(request, 'my_blog/home_page.html')

class PostListView(ListView):
    model = Post
    template_name = 'my_blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

class PostDetailView(DetailView):
    model = Post
    template_name = 'my_blog/post_detail.html'