from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
from .forms import UserForm
from googleapiclient.discovery import build
from application.config import YOUTUBE_API_KEY
from .models import User, Project, Progress, Video

def home(request):
    projects = []  # Default: Empty list of projects

    if request.session.get('user_id'):  # Check if the user is logged in
        user_id = request.session['user_id']
        try:
            # Fetch the logged-in user
            user = User.objects.get(id=user_id)

            # Retrieve projects for the user
            projects = Project.objects.filter(users=user).prefetch_related('progress')

            # Add progress percentages to each project
            for project in projects:
                project.progress_percentages = [p.progress_percentage for p in project.progress.all()]
        except User.DoesNotExist:
            pass

    # Render the home page
    return render(request, 'application/index.html', {'projects': projects})

def user_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UserForm()
    return render(request, 'authentication/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        tel = request.POST.get('tel')
        try:
            user = User.objects.get(name=name, tel=tel)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return JsonResponse({'success': True, 'user_name': user.name})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
    return render(request, 'authentication/login.html')

def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # Remove user ID from session
        del request.session['user_name']  # Remove user name from session
    logout(request)  # Optional: Clear additional session data
    return redirect('/')  # Redirect to home or login page

def team(request):
    return render(request, 'application/team.html')


def watch(request):
    return render(request, 'application/watch.html')

# def search(request):
#     if request.session.get('user_id'):  # Check if the user is logged in
#         user_id = request.session['user_id']
#         # Fetch the logged-in user
#         user = User.objects.get(id=user_id)
#     if request.method == "POST":
#         # Handle Project
#         project = None
#         if request.POST.get('existing_project'):
#             project_id = request.POST['existing_project']
#             project = Project.objects.get(id=project_id)
#         elif request.POST.get('new_project_title'):
#             new_project_title = request.POST['new_project_title']
#             new_project_description = request.POST['new_project_description']
#             project = Project.objects.create(title=new_project_title, description=new_project_description)
#             project.users.set([user])
#         # Handle Videos
#         if project and 'video_id[]' in request.POST:
#             video_ids = request.POST.getlist('video_id[]')
#             video_titles = request.POST.getlist('video_title[]')
#             for video_id, video_title in zip(video_ids, video_titles):
#                 video = Video.objects.create(video_id=video_id, title=video_title)
#                 video.projects.set([project])

#         return redirect('home')  # Redirect to home or a success page

#     # Pass existing projects to the template
#     if request.session.get('user_id'):  # Check if the user is logged in
#         user_id = request.session['user_id']
#         try:
#             # Fetch the logged-in user
#             user = User.objects.get(id=user_id)

#             # Retrieve projects for the user
#             projects = Project.objects.filter(users=user)
#         except User.DoesNotExist:
#             pass
#     return render(request, 'application/search.html', {'projects': projects})

def search_videos(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=7
    )
    response = request.execute()
    return response['items']

def search_playlists(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="playlist",
        maxResults=2
    )
    response = request.execute()
    return response['items']

def get_videos_in_playlist(playlist_id):
    # print(playlist_id)
    # print(YOUTUBE_API_KEY)
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    videos = []
    try:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()
        # print(response)
        for item in response.get('items', []):
            video_id = item['snippet']['resourceId']['videoId']
            # print(video_id)
            title = item['snippet']['title']
            # print(title)
            thumbnail = item['snippet']['thumbnails']['medium']['url']
            # print(thumbnail)
            videos.append({
                "videoId": video_id,
                "title": title,
                "thumbnail": thumbnail
            })
    except Exception as e:
        print(f"Error fetching videos in playlist: {e}")

    # print(videos)
    return videos

def search(request):
    query = request.GET.get('q', '')
    videos = []
    playlists = []
    projects = []
    user = None

    if request.session.get('user_id'):
        user_id = request.session['user_id']
        try:
            user = User.objects.get(id=user_id)
            projects = Project.objects.filter(users=user)
        except User.DoesNotExist:
            pass

    if query:
        videos = search_videos(query)
        # playlists = search_playlists(query)

        # for playlist in playlists:
        #     playlist_id = playlist['id']['playlistId']
        #     playlist_videos = get_videos_in_playlist(playlist_id)
        #     playlist['videos'] = playlist_videos

    if request.method == "POST":
        project = None
        if request.POST.get('existing_project'):
            project_id = request.POST['existing_project']
            project = Project.objects.get(id=project_id)
        elif request.POST.get('new_project_title'):
            new_project_title = request.POST['new_project_title']
            new_project_description = request.POST['new_project_description']
            project = Project.objects.create(title=new_project_title, description=new_project_description)
            project.users.set([user])

        if project and 'video_id[]' in request.POST:
            video_ids = request.POST.getlist('video_id[]')
            video_titles = request.POST.getlist('video_title[]')
            for video_id, video_title in zip(video_ids, video_titles):
                video = Video.objects.create(video_id=video_id, title=video_title)
                video.projects.set([project])

        return redirect('home')

    # for playlist in playlists:
    #     print(playlist)
    
    return render(request, 'application/search.html', {
        'videos': videos,
        'playlists': playlists,
        'query': query,
        'projects': projects
    })