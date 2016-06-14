import datetime
from dateutil.parser import parse
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from charityadmin.apps.timeslots.models import days_of_week_choices, days_of_week_list, Client, Volunteer, ClientOpening, ClientOpeningMetadata, VolunteerCommitment, VolunteerCommitmentMetadata
from charityadmin.apps.timeslots.widgets import SplitDateTimeFieldWithLabels


class UserForm(forms.Form):
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)


class ClientForm(forms.ModelForm):
    # for admin eyes only
    class Meta:
        model = Client
        fields = '__all__'


class VolunteerForm(forms.ModelForm):
    # for admin eyes only
    class Meta:
        model = Volunteer
        fields = '__all__'


class VolunteerSignupForm(forms.ModelForm):
    # this one is end-user facing
    email = forms.EmailField(max_length=100, required=True)
    email_confirm = forms.EmailField(max_length=100, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=100, widget=forms.widgets.PasswordInput())
    
    class Meta:
        model = Volunteer
        # exclude = ['user', 'trained', 'clients']
        fields = ['first_name', 'last_name', 'email', 'email_confirm', 'password', 'phone']
        
    def __init__(self, *args, **kwargs):
        super(VolunteerSignupForm, self).__init__(*args, **kwargs)
        self.fields['email_confirm'].label = "Confirm Email"
        if (self.instance.pk):
            user = self.instance.user
            self.initial['email'] = user.email
            self.initial['first_name'] = user.first_name
            self.initial['last_name'] = user.last_name
        
    def clean_password(self):
        if not self.instance.pk and not self.cleaned_data['password']:
            raise forms.ValidationError("Password is required")
        return self.cleaned_data['password']
        
    def clean(self):
        if not self.cleaned_data['email'] == self.cleaned_data['email_confirm']:
            raise forms.ValidationError("Please confirm your email addresses match")
        return self.cleaned_data
        
    def save(self, commit=True):
        if (self.instance.pk):
            # Editing an existing Volunteer
            user = self.instance.user
            changed = False
            if self.cleaned_data['email'] != user.email:
                user.email = self.cleaned_data['email']
                changed = True
            if self.cleaned_data['first_name'] != user.first_name:
                user.first_name = self.cleaned_data['first_name']
                changed = True
            if self.cleaned_data['last_name'] != user.last_name:
                user.last_name = self.cleaned_data['last_name']
                changed = True
            if changed:
                user.save()
        else:
            # Creating a new volunteer
            first = self.cleaned_data['first_name']
            last = self.cleaned_data['last_name']
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            user, created = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': first, 'last_name': last, 'password': make_password(password)})
            vol = super(VolunteerSignupForm, self).save(commit=False)
            vol.user = user
        super(VolunteerSignupForm, self).save(commit=commit)
        

class OpeningExceptionForm(forms.Form):
    clientOpening = forms.CharField(max_length=10, widget=forms.widgets.HiddenInput())
    date = forms.DateTimeField(widget=forms.widgets.HiddenInput())


class CommitmentExceptionForm(forms.Form):
    commitment = forms.CharField(max_length=10, widget=forms.widgets.HiddenInput())
    date = forms.DateTimeField(widget=forms.widgets.HiddenInput())


class OpeningForm(forms.ModelForm):
    time = forms.CharField(max_length=10, label="Arrival Time", required=False)
    metadata = forms.CharField(max_length=30, required=False)
    # for days of week, alternating days of week
    daysOfWeek = forms.MultipleChoiceField(label="Days of Week", widget=forms.widgets.CheckboxSelectMultiple(), choices=days_of_week_choices, required=False)
    # for day of month
    dayOfMonth = forms.CharField(label="Day of Month (ex: 15)", max_length=2, required=False)
    # for one off date
    oneOffDate = forms.DateField(label="One-Off Date (ex: 12/31/13)", required=False)

    class Meta:
        model = ClientOpening
        fields = ('client', 'type', 'daysOfWeek', 'dayOfMonth', 'oneOffDate', 'metadata', 'time', 'startDate', 'endDate', 'notes')
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
        if self.initial['startDate'] is not None:
            self.initial['time'] = self.initial['startDate'].time()


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

        # on clean, set the StartDate time based on the time field
        # and the EndDate time to midnight
        if self.cleaned_data['time']:
            time = self.cleaned_data['time']
            try:
                time = parse(time)
            except ValueError:
                raise forms.ValidationError("Arrival Time requires a standard time format (e.g., 9:00pm or 10am)")
            self.cleaned_data['time'] = time
            self.cleaned_data['startDate'] = self.cleaned_data['startDate'].replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)
            if self.cleaned_data['endDate'] is not None:
                self.cleaned_data['endDate'] = self.cleaned_data['endDate'].replace(hour=23, minute=59, second=59, microsecond=0)
        else:
            raise forms.ValidationError("The Arrival Time is required")

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
        # set start and end date times correctly
        self.cleaned_data['startDate'] = self.cleaned_data['startDate'].replace(hour=0, minute=0, second=0, microsecond=0)
        if self.cleaned_data['endDate']:
            self.cleaned_data['endDate'] = self.cleaned_data['endDate'].replace(hour=11, minute=59, second=59, microsecond=0)
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
