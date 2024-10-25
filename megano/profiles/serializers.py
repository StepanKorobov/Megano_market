from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from .models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    """
    Сериализатор аватара
    """

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def update(self, instance, validated_data):
        instance.src = validated_data.get("src", instance.src)
        instance.alt = validated_data.get("alt", instance.alt)
        instance.save()

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля
    """

    avatar = AvatarSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["fullName", "phone", "email", "avatar"]


class PasswordSerializer(serializers.Serializer):
    """
    Сериализатор пароля
    """

    currentPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True)

    def validate_currentPassword(self, value):
        user = self.context["request"].user

        if not check_password(value, user.password):
            raise serializers.ValidationError("current password is wrong")

        return value

    def validate_newPassword(self, value):
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["newPassword"])
        user.save()

        return user
