from django.db import models

# User model
class User(models.Model):
    id = models.AutoField(primary_key=True)  # Add ID as primary key
    name = models.CharField(max_length=255, unique=True)
    tel = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

# Project model
class Project(models.Model):
    id = models.AutoField(primary_key=True)  # Add ID as primary key
    users = models.ManyToManyField(User, related_name='projects')  # Change to Many-to-Many relationship
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Video model
class Video(models.Model):
    id = models.AutoField(primary_key=True)  # Add ID as primary key
    projects = models.ManyToManyField(Project, related_name='videos')  # Change to Many-to-Many relationship
    video_id = models.CharField(max_length=20)  # YouTube video ID (11 characters typical)
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_id

# Progress model
class Progress(models.Model):
    id = models.AutoField(primary_key=True)  # Add ID as primary key
    projects = models.ManyToManyField(Project, related_name='progress')  # Change to Many-to-Many relationship
    description = models.TextField()
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # e.g., 85.50 for 85.5%
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress ID: {self.id} - {self.progress_percentage}%"
