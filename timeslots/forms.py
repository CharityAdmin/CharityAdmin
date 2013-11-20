from django.db import models
from django import forms
from django.contrib.auth.models import User
from timeslots.models import Client, Volunteer, ClientOpening, ClientOpeningMetadata, VolunteerCommitment, VolunteerCommitmentMetadata

USER_TYPE_CHOICES = (
    ('VOLUNTEER', 'Volunteer'),
    ('CLIENT', 'Client'),
)

class UserForm(forms.Form):
    type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer

class OpeningForm(forms.ModelForm):
    metadata = forms.CharField(max_length=30)

    class Meta:
        model = ClientOpening

    def __init__(self, *args, **kwargs):
        # patch the initial data to include the metadata values
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.initial['metadata'] = self.instance.get_all_metadata_string()


    def save(self, commit=True):
        # on save, wipe out the existing metadatas and create new ones
        self.instance.clientopeningmetadata_set.all().delete()
        type = self.cleaned_data['type']
        metadatastring = self.cleaned_data['metadata']
        metadata = list()
        if type == "Days of Week" or type == "Days of Alt Week":
            # convert metadata string to list of days
            for day in ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']:
                if metadatastring.find(day) != -1:
                    metadata.append(day)
        else:
            metadata = metadatastring
        for item in metadata:
            md = ClientOpeningMetadata.objects.create(clientOpening=self.instance, metadata=item)
        super(OpeningForm, self).save(commit=commit)

class CommitmentForm(forms.ModelForm):
    class Meta:
        model = VolunteerCommitment

class CommitmentMetadataForm(forms.Form):
    clientOpening = forms.IntegerField()
    metadata = forms.CharField()