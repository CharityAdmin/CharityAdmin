import datetime
from django.db import models
from django import forms
from django.contrib.auth.models import User
from timeslots.models import days_of_week_choices, days_of_week_list, Client, Volunteer, ClientOpening, ClientOpeningMetadata, VolunteerCommitment, VolunteerCommitmentMetadata
from timeslots.widgets import SplitDateTimeFieldWithLabels


class UserForm(forms.Form):
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer


# class OpeningExceptionForm(forms.ModelForm):
#     class Meta:
#         model = ClientOpeningException

#     def __init__(self, *args, **kwargs):
#         super(OpeningExceptionForm, self).__init__(*args, **kwargs)
#         self.fields['clientOpening'].widget = forms.HiddenInput()
#         self.fields['date'].widget = forms.HiddenInput()


class OpeningExceptionForm(forms.Form):
    clientOpening = forms.CharField(max_length=10, widget=forms.widgets.HiddenInput())
    date = forms.DateTimeField(widget=forms.widgets.HiddenInput())


class CommitmentExceptionForm(forms.Form):
    commitment = forms.CharField(max_length=10, widget=forms.widgets.HiddenInput())
    date = forms.DateTimeField(widget=forms.widgets.HiddenInput())


class OpeningForm(forms.ModelForm):
    metadata = forms.CharField(max_length=30, required=False)
    # for days of week, alternating days of week
    daysOfWeek = forms.MultipleChoiceField(label="Days of Week", widget=forms.widgets.CheckboxSelectMultiple(), choices=days_of_week_choices, required=False)
    # for day of month
    dayOfMonth = forms.CharField(label="Day of Month (ex: 15)", max_length=2, required=False)
    # for one off date
    oneOffDate = forms.DateField(label="One-Off Date (ex: 12/31/13)", required=False)

    class Meta:
        model = ClientOpening
        fields = ('client', 'type', 'daysOfWeek', 'dayOfMonth', 'oneOffDate', 'metadata', 'startDate', 'endDate', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'cols': 80, 'rows': 4, 'class': 'notes'}),
            'startDate': SplitDateTimeFieldWithLabels(),
            'endDate': SplitDateTimeFieldWithLabels()
        }

    def __init__(self, *args, **kwargs):
        # patch the initial data to include the metadata values
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.initial['metadata'] = self.instance.get_all_metadata_string()
        metadataset = self.instance.get_all_metadata_list()
        openingtype = self.initial['type']
        if len(metadataset) > 0:
            if openingtype in ["Days of Week", "Days of Alt Week"]:
                self.initial['daysOfWeek'] = metadataset
            elif openingtype == "One-Off":
                self.initial['oneOffDate'] = list(metadataset)[0]
            else:
                self.initial['dayOfMonth'] = list(metadataset)[0]
        # self.fields['metadata'].widget.attrs['class'] = 'hidden'
        self.fields['client'].widget.attrs['class'] = 'hidden'
        self.fields['metadata'].widget.attrs['class'] = 'hidden'

    def clean(self):
        commitmenttype = self.cleaned_data['type']
        if commitmenttype in ["Days of Week", "Days of Alt Week"]:
            self.cleaned_data['metadata'] = ''.join(self.cleaned_data['daysOfWeek'])
        elif commitmenttype == "One-Off":
            specificDate = self.cleaned_data['oneOffDate']
            self.cleaned_data['metadata'] = specificDate.strftime('%Y-%m-%d')
        else:
            # Day of Month
            specificDate = self.cleaned_data['dayOfMonth']
            err_message = "Day of Month Openings require a number between 1 and 31"
            try:
                specific_int = int(specificDate)
            except ValueError:
                raise forms.ValidationError(err_message)
            if not (1 <= specific_int <= 31):
                raise forms.ValidationError(err_message)
            self.cleaned_data['metadata'] = specific_int
        return self.cleaned_data

    def save(self, commit=True):
        # on save, wipe out the existing metadatas and create new ones
        self.instance.metadata.all().delete()
        type = self.cleaned_data['type']
        metadatastring = self.cleaned_data['metadata']
        metadata = list()
        if type == "Days of Week" or type == "Days of Alt Week":
            # convert metadata string to list of days
            for day in days_of_week_list:
                if metadatastring.find(day) != -1:
                    metadata.append(day)
        else:
            metadata = [metadatastring]
        for item in metadata:
            md = ClientOpeningMetadata.objects.create(clientOpening=self.instance, metadata=item)
        return super(OpeningForm, self).save(commit=commit)


class CommitmentForm(forms.ModelForm):
    metadata = forms.CharField(max_length=30, required=False)
    # for days of week, alternating days of week
    daysOfWeek = forms.MultipleChoiceField(label="Days of Week", widget=forms.widgets.CheckboxSelectMultiple(), choices=days_of_week_choices, required=False)
    # for day of month
    dayOfMonth = forms.CharField(label="Day of Month (ex: 15)", max_length=2, required=False)
    # for one off date
    oneOffDate = forms.DateField(label="One-Off Date (ex: 12/31/13)", required=False)

    class Meta:
        model = VolunteerCommitment
        fields = ('clientOpening', 'volunteer', 'type', 'daysOfWeek', 'dayOfMonth', 'oneOffDate', 'metadata', 'startDate', 'endDate', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'cols': 80, 'rows': 4, 'class': 'notes'}),
            'startDate': SplitDateTimeFieldWithLabels(),
            'endDate': SplitDateTimeFieldWithLabels()
        }

    def __init__(self, *args, **kwargs):
        # patch the initial data to include the metadata values
        super(CommitmentForm, self).__init__(*args, **kwargs)
        self.initial['metadata'] = self.instance.get_all_metadata_string()
        metadataset = self.instance.get_all_metadata_list()
        commitmenttype = self.initial['type']
        opening = ClientOpening.objects.get(id=self.initial['clientOpening'])
        if commitmenttype in ["Days of Week", "Days of Alt Week"]:
            # days of week
            if len(metadataset) > 0:
                self.initial['daysOfWeek'] = metadataset
            choicessubset = ((k, k) for k in opening.get_all_metadata_list())
            self.fields['daysOfWeek'].choices = choicessubset
        elif commitmenttype == "One-Off":
            # one-off
            self.initial['oneOffDate'] = list(opening.get_all_metadata_list())[0]
            self.fields['startDate'].widget.attrs['class'] = 'hidden'
            self.fields['endDate'].widget.attrs['class'] = 'hidden'
        else:
            # day of month
            if len(metadataset) > 0:
                self.initial['dayOfMonth'] = list(metadataset)[0]
        self.fields['clientOpening'].widget.attrs['class'] = 'hidden'
        self.fields['volunteer'].widget.attrs['class'] = 'admin-only'
        self.fields['type'].widget.attrs['class'] = 'hidden'
        self.fields['metadata'].widget.attrs['class'] = 'hidden'
        self.fields['dayOfMonth'].widget.attrs['class'] = 'hidden'
        self.fields['oneOffDate'].widget.attrs['class'] = 'hidden'

    def clean_type(self):
        # get type from clientopening (we might want to make commitments have different types than openings, but for now lets keep it simple)
        opening = self.cleaned_data['clientOpening']
        return opening.type

    def clean(self):
        commitmenttype = self.cleaned_data['type']
        if commitmenttype in ["Days of Week", "Days of Alt Week"]:
            self.cleaned_data['metadata'] = ''.join(self.cleaned_data['daysOfWeek'])
        elif commitmenttype == "One-Off":
            # specificDate = self.cleaned_data['oneOffDate']
            # try:
            #     datetime.datetime.strptime(specificDate, '%Y-%m-%d')
            # except ValueError:
            #     raise forms.ValidationError("One-Off Openings require a date in the format YYYY-MM-DD")
            self.cleaned_data['metadata'] = self.cleaned_data['clientOpening'].get_all_metadata_list()
        else:
            # Day of Month
            specificDate = self.cleaned_data['dayOfMonth']
            err_message = "Day of Month Openings require a number between 1 and 31"
            try:
                specific_int = int(specificDate)
            except ValueError:
                raise forms.ValidationError(err_message)
            if not (1 <= specific_int <= 31):
                raise forms.ValidationError(err_message)
            self.cleaned_data['metadata'] = specific_int
        if not self.cleaned_data['metadata']:
            raise forms.ValidationError("The metadata field is required.")
        return self.cleaned_data

    def save(self, commit=True):
        # on save, wipe out the existing metadatas and create new ones
        self.instance.metadata.all().delete()
        metadatastring = self.cleaned_data['metadata']
        metadata = list()
        commitmenttype = self.cleaned_data['type']
        if commitmenttype == "Days of Week" or commitmenttype == "Days of Alt Week":
            # convert metadata string to list of days
            for day in days_of_week_list:
                if metadatastring.find(day) != -1:
                    metadata.append(day)
        else:
            metadata = metadatastring
        for item in metadata:
            md = VolunteerCommitmentMetadata.objects.create(volunteerCommitment=self.instance, metadata=item)
        return super(CommitmentForm, self).save(commit=commit)
