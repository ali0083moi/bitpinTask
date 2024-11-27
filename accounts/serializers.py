from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        try:
            validate_password(data["password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return data

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user
