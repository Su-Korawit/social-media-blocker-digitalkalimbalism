from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
from .forms import UserForm
from .models import User, Project

def home(request):
    if request.session.get('user_id'):  # Check if the user is logged in
        user_id = request.session['user_id']
        try:
            user = User.objects.get(id=user_id)  # Fetch the logged-in user
            projects = Project.objects.filter(user=user)  # Retrieve projects for the user
        except User.DoesNotExist:
            projects = []  # If user does not exist, return an empty list
    else:
        projects = []  # If not logged in, return an empty list

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

def search(request):
    return render(request, 'application/search.html')

def watch(request):
    return render(request, 'application/watch.html')