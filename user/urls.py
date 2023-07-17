from django.urls import path
from user.views import UserCreateView, CreateTokenView, UserLogoutView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", CreateTokenView.as_view(), name="token"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]

app_name = "user"
