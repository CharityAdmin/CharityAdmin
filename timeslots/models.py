from datetime import datetime
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


class Client(models.Model):
    user = models.OneToOneField(User, db_column='userId')

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name if (
        self.user.first_name or self.user.last_name) else self.user.email


class ClientOpening(models.Model):
    client = models.ForeignKey(Client, db_column='clientId')
    startDate = models.DateTimeField('Start Date', default=datetime.now)
    endDate = models.DateTimeField('End Date', blank=True, null=True)
    type = models.CharField(max_length=20, choices=SCHEDULE_PATTERN_TYPE_CHOICES, default='Days of Week')
    notes = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return "%s, %s: %s (%s-%s)" % (
        self.client, self.type, self.clientopeningmetadata_set.all()[0].metadata, dateformat.format(d=self.startDate),
        dateformat.format(d=self.endDate) if self.endDate is not None else "")


class ClientOpeningMetadata(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    metadata = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s, %s: %s" % (self.clientOpening.client, self.clientOpening.type, self.metadata)


class ClientOpeningException(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    date = models.DateTimeField('Exception Date')

    def __unicode__(self):
        return "On %s, client exception to %s" % (datetimeformat.format(d=self.date), self.clientOpening)


class VolunteerCommitment(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    volunteer = models.ForeignKey(Volunteer, db_column='volunteerId')
    startDate = models.DateTimeField('Start Date', default=datetime.now)
    endDate = models.DateTimeField('End Date', blank=True, null=True)
    type = models.CharField(max_length=20, choices=SCHEDULE_PATTERN_TYPE_CHOICES, default='Days of Week')
    notes = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return "%s visits %s, %s: %s (%s-%s)" % (
        self.volunteer, self.clientOpening.client, self.type, self.volunteercommitmentmetadata_set.all()[0].metadata,
        dateformat.format(d=self.startDate), dateformat.format(d=self.endDate) if self.endDate is not None else "")


class VolunteerCommitmentMetadata(models.Model):
    volunteerCommitment = models.ForeignKey(VolunteerCommitment, db_column='volunteerCommitmentId')
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
