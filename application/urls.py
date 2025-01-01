from django.urls import path
from .views import home, user_register, user_login, user_logout, team, search, watch

urlpatterns = [
    path('', home, name='home'),
    path('team/', team, name='team'),
    path('search/', search, name='search'),
    path('watch/<int:id>/', watch, name='watch'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
