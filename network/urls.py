
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_Post", views.new_Post, name="new_Post"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("follow_user", views.follow_user, name="follow_user"),
    path("unfollow_user", views.unFollow_user, name="unfollow_user"),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("add_like/<int:post_id>", views.add_like, name="add_like"),
    path("remove_like/<int:post_id>", views.remove_like, name="remove_like")
]
