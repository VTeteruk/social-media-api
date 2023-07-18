from rest_framework import serializers
from social_media.models import Post


class PostSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "creator",
            "name",
            "content",
            "image",
            "created_date",
            "updated_date",
        )
        read_only_fields = ("id", "creator", "created_date", "updated_date")

    def get_creator(self, obj):
        return obj.creator.email
