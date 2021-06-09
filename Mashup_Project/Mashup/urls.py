from . import views as mashup_views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', mashup_views.index, name='index'),
    path('register/', mashup_views.register, name='register'),
    path('profile/', mashup_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='Mashup/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Mashup/logout.html'), name='logout'),
]

##test