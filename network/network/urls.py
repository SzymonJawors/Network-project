
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_post/', views.create_post, name='create_post'),
    path("all_posts/", views.all_posts, name="all_posts"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path('follow/<str:username>/', views.follow, name='follow'),
    path("following", views.following, name="following"),
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path('like/<int:post_id>/', views.like, name='like'),
]
