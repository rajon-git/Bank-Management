
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.UserBankAccountUpdateView.as_view(), name="profile"),
]
