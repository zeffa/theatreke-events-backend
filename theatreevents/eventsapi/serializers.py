from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from theatreevents.authentication.serializers import UserSerializer
from . import models
from .models import Client


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    phone_number = PhoneNumberField(region='KE')

    class Meta:
        model = models.Client
        fields = ['id', 'name', 'email', 'phone_number', 'approval_status', 'created_at', 'updated_at']


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Venue
        fields = ['id', 'name', 'physical_address', 'capacity']


class ApprovalSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Client.STATUSES)
    comment = serializers.CharField(required=True, max_length=255)


class EventSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    venue = VenueSerializer()
    created_by = UserSerializer()

    class Meta:
        model = models.Event
        fields = '__all__'
