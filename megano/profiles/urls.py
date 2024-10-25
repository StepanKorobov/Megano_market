from django.urls import path

from .views import ProfileUpdateAvatarView, ProfileUpdatePasswordView, ProfileView

app_name = "profiles"

urlpatterns = [
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/password", ProfileUpdatePasswordView.as_view(), name="password"),
    path("profile/avatar", ProfileUpdateAvatarView.as_view(), name="avatar"),
]
