from django.contrib import admin
from .models import User, Project, Video, Progress

# Customize the User admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tel')  # Display these fields in the admin list view
    search_fields = ('name', 'tel')  # Add a search bar for these fields

# Customize the Project admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'updated_at')  # Fields to display
    search_fields = ('title', 'description')  # Search bar for these fields
    filter_horizontal = ('users',)  # Add a horizontal filter for ManyToManyField (users)
    list_filter = ('created_at', 'updated_at')  # Filter by date fields

# Customize the Video admin
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_id', 'title', 'created_at')  # Fields to display
    search_fields = ('video_id', 'title')  # Add search bar
    filter_horizontal = ('projects',)  # Add a horizontal filter for ManyToManyField (projects)
    list_filter = ('created_at',)  # Add a filter for created date

# Customize the Progress admin
@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'progress_percentage', 'created_at', 'updated_at')  # Fields to display
    search_fields = ('description',)  # Add search bar
    filter_horizontal = ('projects',)  # Add a horizontal filter for ManyToManyField (projects)
    list_filter = ('created_at', 'updated_at')  # Filter by date fields
