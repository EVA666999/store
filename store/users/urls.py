from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .views import EmailVerificationView

app_name = "users"


urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.UserRegistrationView.as_view(), name="signup"),
    path(
        "profile/<int:pk>/",
        login_required(views.UserProfileView.as_view()),
        name="profile",
    ),
    path("logout/", views.logout, name="logout"),
    path(
        "verify/<str:email>/<uuid:code>/",
        EmailVerificationView.as_view(),
        name="email_verification",
    ),
]
