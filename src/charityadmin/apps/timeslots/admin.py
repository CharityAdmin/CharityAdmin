from django.contrib import admin
from charityadmin.apps.timeslots.models import *

admin.site.register(Volunteer)
admin.site.register(Client)
admin.site.register(ClientOpening)
admin.site.register(ClientOpeningMetadata)
admin.site.register(ClientOpeningException)
admin.site.register(VolunteerCommitment)
admin.site.register(VolunteerCommitmentMetadata)
admin.site.register(VolunteerCommitmentException)
