from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from django.contrib.auth import logout, get_user_model
from rest_framework.viewsets import ModelViewSet

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    UserDetailSerializer,
    FollowersSerializer, FollowingSerializer,
)


class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        user = self.get_object()
        if user != self.request.user or self.request.user.is_staff:
            raise PermissionDenied(
                "You do not have permission to update this user."
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance != self.request.user or self.request.user.is_staff:
            raise PermissionDenied(
                "You do not have permission to delete this user."
            )
        instance.delete()

    def get_queryset(self):
        email = self.request.query_params.get("email")
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if email:
            self.queryset = get_user_model().objects.filter(
                email__icontains=email
            )
        if first_name:
            self.queryset = get_user_model().objects.filter(
                first_name__icontains=first_name
            )
        if last_name:
            self.queryset = get_user_model().objects.filter(
                last_name__icontains=last_name
            )

        return self.queryset

    def get_serializer_class(self):
        if self.action != "list":
            return UserDetailSerializer
        return UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class UserLogoutView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        # Delete the authentication token associated with the user
        request.user.auth_token.delete()

        logout(request)

        return Response({"detail": "User logged out successfully"})


@api_view(["GET"])
def follow_user(request, pk):
    try:
        user_to_follow = get_user_model().objects.get(pk=pk)
        user = request.user

        if user == user_to_follow:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user in user_to_follow.followed_by.all():
            user_to_follow.followed_by.remove(user)
            message = "User unfollowed successfully."
        else:
            user_to_follow.followed_by.add(user)
            message = "User followed successfully."

        return Response({"message": message}, status=status.HTTP_200_OK)

    except get_user_model().DoesNotExist:
        return Response(
            {"error": "User with the specified ID does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
def followers(request, pk):
    user = get_user_model().objects.get(pk=pk)
    serializer = FollowersSerializer(user)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def following(request, pk):
    user = get_user_model().objects.get(pk=pk)
    serializer = FollowingSerializer(user)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )
