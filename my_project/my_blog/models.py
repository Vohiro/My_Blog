from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish'] # sort result by published field (descending order: newest to oldest)
        indexes = [models.Index(fields=['-publish']),] # to imporve performance for queries filtering

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
