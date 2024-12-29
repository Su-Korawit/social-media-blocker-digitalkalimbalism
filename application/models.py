from django.db import models

# User model
class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tel = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

# Project model
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Video model
class Video(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos')
    video_id = models.CharField(max_length=20)  # YouTube video ID (11 characters typical)
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_id

# Progress model
class Progress(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='progress')
    description = models.TextField()
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # e.g., 85.50 for 85.5%
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.title} - {self.progress_percentage}%"