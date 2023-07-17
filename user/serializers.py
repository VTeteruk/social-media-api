from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("email", "first_name", "last_name", "password")
