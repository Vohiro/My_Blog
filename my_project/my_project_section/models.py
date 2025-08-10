from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import os
import subprocess
from django.conf import settings



class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='publish') # prevent saving new post with the same slug for a given date
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Project_post')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    video = models.FileField(upload_to='videos/')
    preview_video = models.FileField(upload_to='videos/previews/', blank=True, null=True)

    class Meta:
        ordering = ['-publish'] # sort result by published field (descending order: newest to oldest)
        indexes = [models.Index(fields=['-publish']),] # to imporve performance for queries filtering

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug':self.slug, 'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.video and not self.preview_video:
            # Ensure preview path exists
            preview_dir = os.path.join(settings.MEDIA_ROOT, 'videos/previews')
            os.makedirs(preview_dir, exist_ok=True)

            # Define preview file path
            video_path = self.video.path
            preview_filename = f"preview_{os.path.basename(video_path)}"
            preview_path = os.path.join(preview_dir, preview_filename)

            # FFmpeg command: take first 10 seconds
            command = [
                'ffmpeg',
                '-i', video_path,
                '-t', '10',         # Duration
                '-c', 'copy',       # No re-encoding for speed
                preview_path
            ]

            try:
                subprocess.run(command, check=True)
                # Save preview path in model
                self.preview_video.name = f"videos/previews/{preview_filename}"
                super().save(update_fields=['preview_video'])
            except subprocess.CalledProcessError:
                print("Error generating preview video.")
    

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f'Comment by {self.name} on {self.project}'
    
    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'id': self.id})