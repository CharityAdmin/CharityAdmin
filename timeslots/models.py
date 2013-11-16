import datetime
from django.db import models
from django.contrib.auth.models import User

SCHEDULE_PATTERN_TYPE_CHOICES = (
    ('One-Off', 'One-Off'),
    ('Days of Week', 'Days of Week'),
    ('Days of Alternating Week', 'Days of Alternating Week'),
    ('Day of Month', 'Day of Month'),
)

dateformat = '{d:%b %d, %Y}'
datetimeformat = '{d:%b %d, %Y} ({d.hour}:{d.minute:02} {d:%p})'


class Volunteer(models.Model):
    user = models.OneToOneField(User, db_column='userId')
    trained = models.BooleanField(default=False)
    clients = models.ManyToManyField('Client', related_name='volunteers')

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name if (
        self.user.first_name or self.user.last_name) else self.user.email

    def get_current_commitments(self):
        from django.db.models import Q

        today = datetime.datetime.today()
        return  self.commitments.filter(Q(endDate__gte=today) | Q(endDate__isnull=True), startDate__lte=today)


class Client(models.Model):
    user = models.OneToOneField(User, db_column='userId')

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name if (
        self.user.first_name or self.user.last_name) else self.user.email


class ClientOpening(models.Model):
    client = models.ForeignKey(Client, db_column='clientId', related_name='openings')
    startDate = models.DateTimeField('Start Date', default=datetime.datetime.now)
    endDate = models.DateTimeField('End Date', blank=True, null=True)
    type = models.CharField(max_length=20, choices=SCHEDULE_PATTERN_TYPE_CHOICES, default='Days of Week')
    notes = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return "%s, %s: %s (%s-%s)" % (self.client, self.type, self.get_all_metadata_string(), dateformat.format(d=self.startDate), dateformat.format(d=self.endDate) if self.endDate is not None else "")

    def client_title(self):
        # For use in the context of a particular client. Same as the __unicode__ title, but missing the "[client name]: " at the beginning
        return "%s: %s (%s-%s)" % (self.type, self.get_all_metadata_string(), dateformat.format(d=self.startDate), dateformat.format(d=self.endDate) if self.endDate is not None else "")

    def get_next_unfilled(self):
        # get list of openings that haven't been filled
        open_metadata_set = self.get_unfilled_metadata_set()

        # TODO: make this respect commitment end dates
        # TODO: check for exceptions too

        next_opening = None

        if len(open_metadata_set):
            # if we have any open metadata, figure out the next day as a datetime object
            if self.type in ["Days of Week", "Days of Alternating Week"]:
                # get the first element in the set (by day-of-the-week order)
                # TODO: make alternating weeks work
                list_of_days = ['M', 'T', 'W', 'TH', 'F', 'SA', 'SU']
                for idx, day in enumerate(list_of_days):
                    if day in open_metadata_set:
                        now = datetime.datetime.now()
                        next_opening = datetime.datetime.now()
                        # adjust the time to match the startDate time
                        next_opening = next_opening.replace(hour=self.startDate.hour, minute=self.startDate.minute, second=self.startDate.second)
                        # adjust the datetime based on the day of the week
                        next_opening = next_opening + datetime.timedelta(days=idx-now.weekday())
                        if now.weekday() >= idx:
                            # if we've passed the correct day, we want the same day next week
                            next_opening = next_opening + datetime.timedelta(weeks=1)
                        break
            elif self.type == "Day of Month":
                # this assumes that Day-of-month type can only hold a single metadata each
                now = datetime.now()
                next_opening = now.replace(day=open_metadata_set[0], hour=self.startDate.hour, minute=self.startDate.minute, second=self.startDate.second)
                if now.day > open_metadata_set[0]:
                    # if we've already passed the correct day of the month, look at next month instead
                    next_opening = next_opening + datetime.timedelta(month=1)
            else:
                # this is a one-off type
                next_opening = self.startDate
        return next_opening

    def is_filled(self):
        return self.next_opening

    def get_all_metadata_set(self):
        return set([ metadataobj.metadata for metadataobj in self.clientopeningmetadata_set.all() ])

    def get_unfilled_metadata_set(self):
        return set([ metadataobj.metadata for metadataobj in self.clientopeningmetadata_set.all() if not metadataobj.is_filled() ])

    def get_all_metadata_string(self):
        if self.type in ["Days of Week", "Days of Alternating Week"]:
            join_string = ''
        else:
            join_string = ', '
        combinedmetadata = join_string.join(self.get_all_metadata_set())
        return combinedmetadata


class ClientOpeningMetadata(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    metadata = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s, %s: %s" % (self.clientOpening.client, self.clientOpening.type, self.metadata)

    def is_filled(self):
        return self.metadata in set([metadataobj.metadata for commitment in self.clientOpening.volunteercommitment_set.all() for metadataobj in commitment.volunteercommitmentmetadata_set.all()])


class ClientOpeningException(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    date = models.DateTimeField('Exception Date')

    def __unicode__(self):
        return "On %s, client exception to %s" % (datetimeformat.format(d=self.date), self.clientOpening)


class VolunteerCommitment(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    volunteer = models.ForeignKey(Volunteer, db_column='volunteerId', related_name="commitments")
    startDate = models.DateTimeField('Start Date', default=datetime.datetime.now)
    endDate = models.DateTimeField('End Date', blank=True, null=True)
    type = models.CharField(max_length=20, choices=SCHEDULE_PATTERN_TYPE_CHOICES, default='Days of Week')
    notes = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return "%s visits %s, %s: %s (%s-%s)" % (
        self.volunteer, self.clientOpening.client, self.type, self.volunteercommitmentmetadata_set.all()[0].metadata,
        dateformat.format(d=self.startDate), dateformat.format(d=self.endDate) if self.endDate is not None else "")

    def pattern_description(self, prefix="Visit "):
        # displays just the Type, Metadata, and Start/End Dates
        return "%s: %s (%s-%s)" % (self.type, self.volunteercommitmentmetadata_set.all()[0].metadata, dateformat.format(d=self.startDate), dateformat.format(d=self.endDate) if self.endDate is not None else "")


class VolunteerCommitmentMetadata(models.Model):
    volunteerCommitment = models.ForeignKey(VolunteerCommitment, db_column='volunteerCommitmentId')
    # FEATURE REQUEST: prettify/validate the metadata field:
    #                  use a select box when the volunteerCommitment is set to day of week,
    #                  calendar when day of month or one-off date
    metadata = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s visits %s, %s: %s" % (
        self.volunteerCommitment.volunteer, self.volunteerCommitment.clientOpening.client,
        self.volunteerCommitment.clientOpening.type, self.metadata)


class VolunteerCommitmentException(models.Model):
    volunteerCommitment = models.ForeignKey(VolunteerCommitment, db_column='volunteerCommitmentId')
    date = models.DateTimeField('Exception Date')

    def __unicode__(self):
        return "On %s, volunteer exception to %s " % (datetimeformat.format(d=self.date), self.volunteerCommitment)
