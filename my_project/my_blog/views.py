from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from django.views.generic.edit import (
    CreateView, 
    UpdateView,
    DeleteView
    )
from django.utils.text import slugify
from django.urls import reverse_lazy

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

class PostCreateView(CreateView):
    model = Post
    template_name = 'my_blog/post_new.html'
    fields = ['author', 'title', 'body']

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)
    
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'my_blog/post_edit.html'
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)
    
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'my_blog/post_delete.html'
    success_url = reverse_lazy('post_list')
