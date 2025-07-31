from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post
from django.views.generic.edit import (
    CreateView, 
    UpdateView,
    DeleteView
    )
from django.utils.text import slugify
from django.urls import reverse_lazy
from .forms import EmailPostForm
from django.core.mail import send_mail

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

def post_share(request, pk):
    post = get_object_or_404(Post, id=pk)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" \
                        f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'vohiro.blog@gmail.com', [cd['to']])
            sent = True 
    else:
        form = EmailPostForm()
    return render(request, 'my_blog/post_share.html', {'post': post,
                                                       'form': form,
                                                       'sent': sent})
