from django.urls import path
from social_media.views import PostListCreateView, PostDetailView

urlpatterns = [
    path("posts", PostListCreateView.as_view(), name="posts"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail")
]

app_name = "post"
