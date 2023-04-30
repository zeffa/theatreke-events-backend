from django.template.loader import render_to_string
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Client, Event, Venue, ApprovalLog
from . import serializers, tasks
from .utils import get_client_code


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        serializer = serializers.ApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        status = serializer.validated_data['status']
        notes = serializer.validated_data['comment']
        if instance.status == status:
            return Response(data={'message': 'Already in the %s status' % status}, status=400)
        instance.status = status
        instance.save()
        # Send an email here to the client to notify them of the approval status
        html_template = 'email_template.html'
        context = {
            'subject': 'Event Approval',
            'heading': 'Theatre Events',
            'title': instance.title,
            'status': status,
            'notes': notes
        }
        html_content = render_to_string(html_template, context)
        tasks.send_email.delay(
            'Event Approval',
            'The approval for %s was %s. %s' % (instance.title, status, notes),
            [instance.client.email],
            html_content=html_content
        )
        approval_log = ApprovalLog(
            approved_by=request.user,
            action=status,
            notes=notes,
            entity='Event',
            item_id=pk,
        )
        approval_log.save()
        data = serializers.EventSerializer(instance).data
        return Response(data=data)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = serializers.ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        serializer = serializers.ApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        status = serializer.validated_data['status']
        notes = serializer.validated_data['comment']
        if instance.approval_status == status:
            return Response(data={'message': 'Already in the %s status' % status}, status=400)
        instance.approval_status = status
        instance.code = get_client_code(instance.name)
        instance.save()
        # Send an email here to the client to notify them of the approval status
        html_template = 'email_template.html'
        context = {
            'subject': 'Client Approval',
            'heading': 'Theatre Events',
            'title': instance.name,
            'status': status,
            'notes': notes
        }
        html_content = render_to_string(html_template, context)
        tasks.send_email.delay(
            'Client Approval',
            'Your approval was %s. %s' % (status, notes),
            [instance.email],
            html_content=html_content
        )
        approval_log = ApprovalLog(
            approved_by=request.user,
            action=status,
            notes=notes,
            entity='Client',
            item_id=pk,
        )
        approval_log.save()
        data = serializers.ClientSerializer(instance).data
        return Response(data=data)


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all().order_by('-created_at')
    serializer_class = serializers.VenueSerializer
    permission_classes = [permissions.IsAuthenticated]
