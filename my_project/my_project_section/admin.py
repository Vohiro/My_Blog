from django.contrib import admin
from .models import Project, Comment

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish']
    list_filter = ['created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['publish']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'project', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)
