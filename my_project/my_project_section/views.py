from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Project
from .forms import CommentForm, EmailPostForm
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

class ProjectListView(ListView):
    model = Project
    template_name = 'my_project_section/project_list.html'
    context_object_name = 'projects'
    paginate_by = 3


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'my_project_section/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        # For comments
        context['comments'] = project.comments.filter(active=True) # To list active comment for this post
        context['form'] = CommentForm() # form for user to fill
        return context


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'my_project_section/project_new.html'
    fields = ['author', 'title', 'video', 'body']

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'my_project_section/project_edit.html'
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)
    

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'my_project_section/project_delete.html'
    success_url = reverse_lazy('project_list')


def project_share(request, pk):
    project = get_object_or_404(Project, id=pk)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project_url = request.build_absolute_uri(project.get_absolute_url())
            subject = f"{cd['name']} recommends you read" \
                        f"{project.title}"
            message = f"Read {project.title} at {project_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'vohiro.blog@gmail.com', [cd['to']])
            sent = True 
    else:
        form = EmailPostForm()
    return render(request, 'my_project_section/project_share.html', {'project': project,
                                                       'form': form,
                                                       'sent': sent})

@require_POST
def project_comment(request, pk):
    project = get_object_or_404(Project, id=pk)
    comment = None

    #To handle a posted comment
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False) # To create a comment object without saving it to database
        comment.project = project # Assign the post to comment
        comment.save() # save comment to database
    context = {'proejct': project, 'form': form, 'comment': comment}
    return render(request, 'my_project_section/project_comment.html', context)