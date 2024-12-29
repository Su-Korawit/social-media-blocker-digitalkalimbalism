from django.contrib import admin
from .models import User, Project, Video, Progress

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Video)
admin.site.register(Progress)
