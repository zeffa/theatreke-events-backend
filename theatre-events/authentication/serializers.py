from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.base_user import BaseUserManager
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'email', 'first_name', 'last_name', 'phone_number', 'client')


class RegistrationSerializer(serializers.ModelSerializer):
    client_code = serializers.CharField(max_length=10, allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'client_code']

    def validate_email(self, email):
        user = User.objects.filter(email=email)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(email)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class RegistrationSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'client']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('user_id', 'email', 'first_name', 'last_name', 'phone_number', 'client', 'admin', 'auth_token')
        read_only_fields = ('user_id', 'is_active', 'staff', 'admin')

    def get_auth_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class EmptySerializer(serializers.Serializer):
    pass
