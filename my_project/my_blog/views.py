from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Comment
from django.views.generic.edit import (
    CreateView, 
    UpdateView,
    DeleteView
    )
from django.utils.text import slugify
from django.urls import reverse_lazy
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

def home_page(request):
    return render(request, 'my_blog/home_page.html')

class PostListView(ListView):
    model = Post
    template_name = 'my_blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.tag = None
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[self.tag])
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context 
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'my_blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # For comments
        context['comments'] = post.comments.filter(active=True) # To list active comment for this post
        context['form'] = CommentForm() # form for user to fill

        # Similar post based on shared tags
        post_tag_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tag_ids)\
            .exclude(id=post.id)\
            .annotate(same_tags=Count('tags'))\
            .order_by('-same_tags', '-created')[:4]
        context['similar_posts'] = similar_posts

        return context

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

@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    comment = None

    #To handle a posted comment
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False) # To create a comment object without saving it to database
        comment.post = post # Assign the post to comment
        comment.save() # save comment to database
    context = {'post': post, 'form': form, 'comment': comment}
    return render(request, 'my_blog/post_comment.html', context)
