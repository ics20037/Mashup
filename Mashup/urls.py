from . import views as mashup_views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', mashup_views.Feed.as_view(), name='index'),
    path('user/<str:username>', mashup_views.UserPostView.as_view(), name='user-posts'),
    path('post/<int:pk>/', mashup_views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', mashup_views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', mashup_views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', mashup_views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', mashup_views.CommentCreateView.as_view(), name='post-comment'),
    path('comment/<int:pk>/update/', mashup_views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', mashup_views.CommentDeleteView.as_view(), name='comment-delete'),
    path('register/', mashup_views.register, name='register'),
    path('profile/', mashup_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='Mashup/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Mashup/logout.html'), name='logout'),
]
