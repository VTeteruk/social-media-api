from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import (
    UserViewSet,
    CreateTokenView,
    UserLogoutView,
    UserCreateView,
    follow_user,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

app_name = "user"

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", CreateTokenView.as_view(), name="token"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("", include(router.urls)),
    path("users/<int:pk>/follow", follow_user, name="follow-user"),
]
