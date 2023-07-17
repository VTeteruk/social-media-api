from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from django.contrib.auth import logout
from user.serializers import UserSerializer, AuthTokenSerializer


class UserCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class UserLogoutView(APIView):

    def get(self, request, *args, **kwargs) -> Response:
        # Delete the authentication token associated with the user
        request.user.auth_token.delete()

        logout(request)

        return Response({'detail': 'User logged out successfully'})
