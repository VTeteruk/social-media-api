from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from social_media.models import Post
from social_media.serializers import PostSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        if name:
            self.queryset = Post.objects.filter(name__icontains=name)
        # Filter posts from both the current user and the users they follow
        user = self.request.user
        return Post.objects.filter(
            Q(creator=user) | Q(creator_id__in=user.follows.all())
        )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description='Filter by post\'s name',
                type=str
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        user = self.get_object()
        if user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied(
                "You do not have permission to update this post."
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied(
                "You do not have permission to delete this post."
            )
        instance.delete()
