from django.urls import path

from .views import SignInView, SignOutView, SignUpView

app_name = "authusers"

urlpatterns = [
    path("sign-in", SignInView.as_view(), name="signin"),
    path("sign-up", SignUpView.as_view(), name="signup"),
    path("sign-out", SignOutView.as_view(), name="signout"),
]
