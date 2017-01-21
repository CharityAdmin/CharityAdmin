from django.contrib import admin

from charityadmin.apps.timeslots.models import *


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'zipcode')


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user', )

admin.site.register(ClientOpening)
admin.site.register(ClientOpeningMetadata)
admin.site.register(ClientOpeningException)
admin.site.register(VolunteerCommitment)
admin.site.register(VolunteerCommitmentMetadata)
admin.site.register(VolunteerCommitmentException)
