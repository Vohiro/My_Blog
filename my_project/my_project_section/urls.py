from django.urls import path
from django.views.generic import TemplateView
from .views import (
    ProjectListView, 
    ProjectDetailView, 
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    project_share,
    project_comment,
    )
    
urlpatterns = [
    path('', TemplateView.as_view(template_name='my_project_section/index.html'), name='project_HomePage'),
    path('list/', ProjectListView.as_view(), name='project_list'),
    path('detail/<slug:slug>/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('create/', ProjectCreateView.as_view(), name='project_new'),
    path('detail/<slug:slug>/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('detail/<slug:slug>/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('detail/<slug:slug>/<int:pk>/share/', project_share, name='project_share'),
    path('detail/<slug:slug>/<int:pk>/comment/', project_comment, name='project_comment'),
]