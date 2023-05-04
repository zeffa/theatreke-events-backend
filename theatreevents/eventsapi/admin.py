from django.contrib import admin

from .models import Client, Event, Venue


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'code', 'approval_status', 'deleted']


class VenueAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'physical_address', 'capacity']


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'date_and_time', 'status', 'sharable_link', 'client', 'venue')


admin.site.register(Event, EventAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Venue, VenueAdmin)
