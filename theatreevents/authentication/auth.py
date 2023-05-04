from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


def authenticate_and_get_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError({"message": "Invalid username or password"})
    return user


def create_user_account(email, password, client=None, first_name=None, last_name=None, **extra_fields):
    user_model = get_user_model()
    user = user_model.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        client=client,
        **extra_fields
    )
    return user
