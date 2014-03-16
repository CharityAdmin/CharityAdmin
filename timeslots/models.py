import datetime
import urllib
from dateutil.rrule import *
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models import Q
from localflavor.us.us_states import STATE_CHOICES

SCHEDULE_PATTERN_TYPE_CHOICES = (
    ('One-Off', 'One-Off'),
    ('Days of Week', 'Days of Week'),
    ('Days of Alt Week', 'Days of Alternating Week'),
    ('Day of Month', 'Day of Month'),
)

dateformat = '{d:%b %d, %Y}'
timeformat = '({d.hour}:{d.minute:02} {d:%p})' # TODO: This shows the time in 24-hours, need to fix.
datetimeformat = '{d:%b %d, %Y} ({d.hour}:{d.minute:02} {d:%p})'

#days_of_week_dict maps our day strings "M", "Tu", ... to the dateutil objects MO, TU, ...
days_of_week_dict = {'M': MO, 'Tu': TU, 'W': WE, 'Th': TH, 'F': FR, 'Sa': SA, 'Su': SU}
days_of_week_list = ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']
days_of_week_choices = (('M', 'Mo'), ('Tu', 'Tu'), ('W', 'We'), ('Th', 'Th'), ('F', 'Fr'), ('Sa', 'Sa'), ('Su', 'Su'))


class Volunteer(models.Model):
    user = models.OneToOneField(User, db_column='userId')
    trained = models.BooleanField(default=False)
    clients = models.ManyToManyField('Client', blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name if (
        self.user.first_name or self.user.last_name) else self.user.email

    def get_absolute_url(self):
        return reverse('timeslots_volunteer_view', kwargs={'userid': self.user.id})

    def get_absolute_edit_url(self):
        return reverse('timeslots_volunteer_edit', kwargs={'userid': self.user.id})

    def get_absolute_list_url(self):
        """ URL for list of Volunteers """
        return reverse('timeslots_volunteers_view')

    def get_clean_model_name(self):
        return "Volunteer"

    def get_current_commitments(self):
        today = timezone.now()
        return self.commitments.filter(Q(endDate__gte=today) | Q(endDate__isnull=True), startDate__lte=today)

    def get_openings(self, client=None):
        today = timezone.now()
        if client:
            client_list = [client]
        else:
            client_list = self.clients.all()
        openings = ClientOpening.objects.filter(Q(endDate__gte=today) | Q(endDate__isnull=True), startDate__lte=today, client__in=client_list)
        return openings

    def get_commitments(self, client=None):
        today = timezone.now()
        if client:
            commitments = self.commitments.filter(Q(endDate__gte=today) | Q(endDate__isnull=True), startDate__lte=today, clientOpening__client=client)
        else:
            commitments = self.commitments.filter(Q(endDate__gte=today) | Q(endDate__isnull=True), startDate__lte=today)
        return commitments

    def get_commitment_instances(self, startDate=None, endDate=None, client=None, **kwargs):
        instances = list()
        for commitment in self.get_commitments(client=client):
            instances.extend(commitment.get_instances(startDate=startDate, endDate=endDate, **kwargs))
        instances.sort(key=lambda item:item['date'])
        return instances

    def get_unfilled_client_opening_instances(self, startDate=None, endDate=None, **kwargs):
        openings = list()
        for opening in ClientOpening.objects.filter(client__volunteers=self):
            openings.extend(opening.get_unfilled_instances(startDate=startDate, endDate=endDate))
        openings.sort(key=lambda item:item['date'])
        return openings


class Client(models.Model):
    user = models.OneToOneField(User, db_column='userId')
    address = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    volunteers = models.ManyToManyField('Volunteer', through=Volunteer.clients.through, blank=True)


    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name if (
        self.user.first_name or self.user.last_name) else self.user.email

    def get_absolute_url(self):
        return reverse('timeslots_client_view', kwargs={'userid': self.user.id})

    def get_absolute_edit_url(self):
        return reverse('timeslots_client_edit', kwargs={'userid': self.user.id})

    def get_absolute_list_url(self):
        """ URL for list of Clients """
        return reverse('timeslots_clients_view')

    def get_clean_model_name(self):
        return "Client"

    def get_opening_instances(self, **kwargs):
        instances = list()
        for opening in self.openings.all():
            instances.extend(opening.get_next_instances(**kwargs))
        instances.sort()
        return instances

    def get_unfilled_opening_instances(self, **kwargs):
        instances = list()
        for opening in self.openings.all():
            instances.extend(opening.get_unfilled_instances(**kwargs))
        instances.sort()
        return instances

    def get_commitments(self, **kwargs):
        openings = self.openings.all()
        commitments = list()
        for opening in openings:
            commitments.extend(opening.volunteercommitment_set.all())
        return commitments

    def get_unfilled_openings(self, **kwargs):
        # this includes all openings for the client which are not ENTIRELY filled
        openings = (x for x in self.openings.all() if not x.is_filled())
        return openings

    def get_address_urlencoded(self, **kwargs):
        # for Google Maps link
        addressString = self.address + ", " + self.city + " " + self.state + " " + self.zipcode
        urlEncoded = urllib.urlencode({ 'q': addressString })
        return urlEncoded


class ClientOpening(models.Model):
    client = models.ForeignKey(Client, db_column='clientId', related_name='openings')
    startDate = models.DateTimeField('Start Date', default=timezone.now().replace(hour=12, minute=0, second=0, microsecond=0))
    endDate = models.DateTimeField('End Date', blank=True, null=True)
    type = models.CharField(max_length=20, choices=SCHEDULE_PATTERN_TYPE_CHOICES, default='Days of Week')
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "%s, %s: %s %s (%s-%s)" % (self.client, self.type, self.get_all_metadata_string(), self.startDate.strftime("%-I:%M %p"), dateformat.format(d=self.startDate), dateformat.format(d=self.endDate) if self.endDate is not None else "")

    def get_absolute_url(self):
        return reverse('timeslots_opening_view', kwargs={'openingid': self.id})

    def get_absolute_edit_url(self):
        return reverse('timeslots_opening_edit', kwargs={'openingid': self.id})

    def get_absolute_list_url(self):
        """ URL for list of Openings """
        return reverse('timeslots_openings_view')

    def get_absolute_list_for_client_url(self):
        """ URL for list of Openings for this client """
        return reverse('timeslots_openings_view', kwargs={'clientid': self.client.user.id})

    def get_clean_model_name(self):
        return "Opening"

    def get_client_title(self):
        # For use in the context of a particular client. Same as the __unicode__ title, but missing the "[client name]: " at the beginning
        return "%s: %s %s (%s-%s)" % (self.type, self.get_all_metadata_string(), self.startDate.strftime("%-I:%M %p"), dateformat.format(d=self.startDate), dateformat.format(d=self.endDate) if self.endDate is not None else "")

    def get_client_name(self):
        return self.client

    def _get_instance_dates(self, count=30, startDate=None, endDate=None, metadata_set=None):
        if startDate is None:
            startDate = self.startDate
        if endDate is None:
            endDate = self.endDate
        if metadata_set is None:
            metadata_set = self.get_all_metadata_list()
        instance_list = list()
        if self.type in ["Days of Week", "Days of Alternating Week"]:
            interval = 2 if self.type == "Days of Alternating Week" else 1
            instance_list = list(rrule(WEEKLY, count=count, byweekday=(days_of_week_dict[day] for day in metadata_set), byhour=self.startDate.hour, byminute=self.startDate.minute, bysecond=self.startDate.second, dtstart=startDate, until=endDate, interval=interval))
        elif self.type == "Day of Month":
            instance_list = list(rrule(MONTHLY, count=count, bymonthday=metadata_set, byhour=self.startDate.hour, byminute=self.startDate.minute, bysecond=self.startDate.second, dtstart=startDate, until=endDate))
        else:
            # this is a one-off type
            instance_list = list([self.startDate])
        return instance_list

    def get_instance(self, instance_date, **kwargs):
        instance = None
        opening_instances = self.get_instances(count=1, startDate=instance_date)
        if len(opening_instances) > 0:
            opening_instance = opening_instances[0]
            if opening_instance["date"] == instance_date:
                instance = opening_instance
        return instance

    def get_unfilled_instances(self, startDate=None, endDate=None, **kwargs):
        if startDate is None:
            startDate = self.startDate
        if endDate is None:
            endDate = self.endDate
        metadata_set = kwargs.pop('metadata_set') if 'metadata_set' in kwargs else self.get_unfilled_metadata_set()
        instance_dates = list()
        if len(metadata_set) > 0:
            instance_dates = self._get_instance_dates(metadata_set=metadata_set, startDate=startDate, endDate=endDate, **kwargs)

        exception_dates = [e.date for e in self.exceptions.all()]

        instances = [{
            "date": instance_date.replace(second=0, microsecond=0),
            "is_filled": False,
            "client": self.client,
            "url": self.get_absolute_url(),
            "openingid": self.id,
            "openingexception": True if instance_date in exception_dates else False
        } for instance_date in instance_dates]

        return instances

    def get_filled_instances(self, startDate=None, endDate=None, **kwargs):
        if startDate is None:
            startDate = self.startDate
        if endDate is None:
            endDate = self.endDate
        metadata_set = kwargs.pop('metadata_set') if 'metadata_set' in kwargs else self.get_filled_metadata_set()
        instance_dates = list()
        if len(metadata_set) > 0:
            instance_dates = self._get_instance_dates(metadata_set=metadata_set, startDate=startDate, endDate=endDate, **kwargs)

        exception_dates = [e.date for e in self.exceptions.all()]

        instances = [{
            "date": instance_date.replace(second=0, microsecond=0),
            "is_filled": True,
            "client": self.client,
            "url": self.get_absolute_url(),
            "openingid": self.id,
            "openingexception": True if instance_date in exception_dates else False
        } for instance_date in instance_dates]

        return instances

    def get_instances(self, startDate=None, endDate=None, **kwargs):
        if startDate is None:
            startDate = self.startDate
        if endDate is None:
            endDate = self.endDate
        filled_instances = self.get_filled_instances(startDate=startDate, endDate=endDate, **kwargs)
        unfilled_instances = self.get_unfilled_instances(startDate=startDate, endDate=endDate, **kwargs)
        instances = list()
        instances.extend(filled_instances)
        instances.extend(unfilled_instances)
        instances.sort(key=lambda item:item['date'])
        # return distinct list of instances (since filled_instance comes first,
        # any overlapping filled and unfilled instance should show as filled)
        seen = set()
        distinct = [instance for instance in instances if instance['date'] not in seen and not seen.add(instance['date'])]
        return distinct

    def get_next_instances(self, startDate=None, endDate=None, **kwargs):
        if startDate is None:
            startDate = timezone.now()
        return self.get_instances(startDate=startDate, endDate=endDate, **kwargs)

    def get_next_unfilled_instances(self, endDate=None, **kwargs):
        return self.get_unfilled_instances(startDate=timezone.now(), endDate=endDate, **kwargs)

    def get_next_unfilled_instance(self, **kwargs):
        return self.get_next_unfilled_instances(count=1, **kwargs)

    def get_all_metadata_list(self):
        allmetadata = [metadataobj.metadata for metadataobj in self.metadata.all()]
        if self.type in ["Days of Week", "Days of Alternating Week"]:
            allmetadata = sorted(allmetadata, key=days_of_week_list.index)
        return allmetadata

    def get_unfilled_metadata_set(self):
        return set([metadataobj.metadata for metadataobj in self.metadata.all() if not metadataobj.is_filled()])

    def get_filled_metadata_set(self):
        return set([metadataobj.metadata for metadataobj in self.metadata.all() if metadataobj.is_filled()])

    def get_all_metadata_string(self):
        if self.type in ["Days of Week", "Days of Alternating Week"]:
            join_string = ''
        else:
            join_string = ', '
        return join_string.join(self.get_all_metadata_list())

    def is_filled(self):
        # Has all instances filled
        return len(self.get_filled_metadata_set()) > 0 and len(self.get_unfilled_metadata_set()) == 0

    def is_partially_filled(self):
        # Has some instances unfilled, some instances filled
        return len(self.get_filled_metadata_set()) > 0 and len(self.get_unfilled_metadata_set()) > 0

    def is_unfilled(self):
        # Has no instances filled
        return len(self.get_unfilled_metadata_set()) > 0 and len(self.get_filled_metadata_set()) is 0

    def is_blank(self):
        # Has no instances filled and no instances unfilled (something is probably wrong)
        return len(self.get_unfilled_metadata_set()) is 0 and len(self.get_filled_metadata_set()) is 0

    def get_filled_status(self):
        value = "empty"
        if self.is_filled():
            value = "filled"
        if self.is_partially_filled():
            value = "partially-filled"
        if self.is_unfilled():
            value = "unfilled"
        return value


class ClientOpeningMetadata(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, related_name="metadata", db_column='clientOpeningId')
    metadata = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s, %s: %s" % (self.clientOpening.client, self.clientOpening.type, self.metadata)

    def is_filled(self):
        return self.metadata in set([metadataobj.metadata for commitment in self.clientOpening.volunteercommitment_set.all() for metadataobj in commitment.metadata.all()])


class ClientOpeningException(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId', related_name="exceptions")
    date = models.DateTimeField('Exception Date')

    def __unicode__(self):
        return "On %s, client exception to %s" % (datetimeformat.format(d=self.date), self.clientOpening)

    def get_instance(self):
        return self.clientOpening.get_instance(self.date)


class VolunteerCommitment(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    volunteer = models.ForeignKey(Volunteer, db_column='volunteerId', related_name="commitments")
    startDate = models.DateTimeField('Start Date', default=datetime.datetime.now)
    endDate = models.DateTimeField('End Date', blank=True, null=True)
    type = models.CharField(max_length=20, choices=SCHEDULE_PATTERN_TYPE_CHOICES, default='Days of Week')
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        title = "%s visits %s, %s: %s (%s-%s)" % (
                    self.volunteer, self.clientOpening.client, self.type, self.get_all_metadata_string(),
                    dateformat.format(d=self.startDate), dateformat.format(d=self.endDate) if self.endDate is not None else ""
                )
        return title

    def get_absolute_url(self):
        return reverse('timeslots_commitment_view', kwargs={'commitmentid': self.id})

    def get_absolute_edit_url(self):
        return reverse('timeslots_commitment_edit', kwargs={'commitmentid': self.id})

    def get_absolute_list_url(self):
        """ URL for list of Commitments """
        return reverse('timeslots_commitments_view')

    def get_absolute_list_for_client_url(self):
        """ URL for list of Commitments for this client """
        return reverse('timeslots_commitments_view', kwargs={'clientid': self.clientOpening.client.user.id})

    def get_clean_model_name(self):
        return "Commitment"

    def get_client_name(self):
        return self.clientOpening.client

    def pattern_description(self, prefix="Visit "):
        # displays just the Type, Metadata, and Start/End Dates
        return "%s: %s (%s-%s)" % (self.type, self.get_all_metadata_string(), dateformat.format(d=self.startDate), dateformat.format(d=self.endDate) if self.endDate is not None else "")

    def get_all_metadata_list(self):
        allmetadata = [metadataobj.metadata for metadataobj in self.metadata.all()]
        if self.type in ["Days of Week", "Days of Alternating Week"]:
            allmetadata = sorted(allmetadata, key=days_of_week_list.index)
        return allmetadata

    def get_all_metadata_string(self):
        if self.type in ["Days of Week", "Days of Alternating Week"]:
            join_string = ''
        else:
            join_string = ', '
        combinedmetadata = join_string.join(self.get_all_metadata_list())
        return combinedmetadata

    def get_instances(self, **kwargs):
        instances = self.clientOpening.get_instances(metadata_set=self.get_all_metadata_list(), **kwargs)
        # get exceptions
        exception_dates = [e.date for e in self.exceptions.all()]
        
        for instance in instances:
            # mark instances with volunteer exceptions
            instance['volunteer'] = self.volunteer;
            instance['commitmentid'] = self.id;
            instance["commitmentexception"] = True if instance['date'] in exception_dates else False
        return instances

    def get_instance(self, instance_date,  **kwargs):
        instance = None
        commitment_instances = self.get_instances(count=1, startDate=instance_date)
        if len(commitment_instances) > 0:
            commitment_instance = commitment_instances[0]
            if commitment_instance["date"] == instance_date:
                instance = commitment_instance
        return instance


class VolunteerCommitmentMetadata(models.Model):
    volunteerCommitment = models.ForeignKey(VolunteerCommitment, related_name="metadata", db_column='volunteerCommitmentId')
    metadata = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s visits %s, %s: %s" % (
        self.volunteerCommitment.volunteer, self.volunteerCommitment.clientOpening.client,
        self.volunteerCommitment.clientOpening.type, self.metadata)


class VolunteerCommitmentException(models.Model):
    volunteerCommitment = models.ForeignKey(VolunteerCommitment, db_column='volunteerCommitmentId', related_name="exceptions")
    date = models.DateTimeField('Exception Date')

    def __unicode__(self):
        return "On %s, volunteer exception to %s " % (datetimeformat.format(d=self.date), self.volunteerCommitment)

    def get_instance(self):
        return self.volunteerCommitment.get_instance(self.date)

#fixme: add actual types
EVENT_TYPE_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

class Event(models.Model):
    client = models.ForeignKey(Client, db_column='clientId', related_name='events', null=True)
    volunteer = models.ForeignKey(Volunteer, db_column='volunteerId', related_name="events", null=True)
    date = models.DateTimeField('Date', default=timezone.now().replace(hour=12, minute=0, second=0, microsecond=0))
    durationInMinutes = models.PositiveIntegerField(null=True)
    type = models.CharField(max_length=255, choices=EVENT_TYPE_CHOICES)
    notes = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return "%s: %s, '%s' '%s'" % (self.type, self.date, self.client, self.volunteer)
