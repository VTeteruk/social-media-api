from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff",
        )
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 3}}

    def create(self, validated_data) -> get_user_model():
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserListSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name")


class UserDetailSerializer(UserSerializer):
    count_followers = serializers.SerializerMethodField()
    count_following = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            "bio",
            "image",
            "count_followers",
            "count_following",
        )

    def get_count_followers(self, obj):
        return obj.count_followers()

    def get_count_following(self, obj):
        return obj.count_following()


class FollowersSerializer(serializers.ModelSerializer):
    followed_by = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("followed_by",)

    def get_followed_by(self, obj):
        followed_by_users = obj.followed_by.all()
        return [user.email for user in followed_by_users]


class FollowingSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("following",)

    def get_following(self, obj):
        following_by_users = obj.follows.all()
        return [user.email for user in following_by_users]
