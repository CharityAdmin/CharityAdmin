from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     TYPE_CHOICES = (
#         ('Admin', 'Admin'),
#         ('Volunteer', 'Volunteer'),
#         ('Client', 'Client'),
#     )

#     user = models.OneToOneField(User)
#     type = models.CharField(max_length=9, choices=TYPE_CHOICES, default='Volunteer')

# class Volunteer(Profile):
#     trained = models.Boolean(default=False)
#     clients = models.ManyToManyField('Client', related_name='volunteers')

#     def __unicode__(self):
#         return (self.user.first_name || self.user.last_name) ? self.user.first_name + " " + self.user.last_name : self.user.email

# class Client(Profile):

#     def __unicode__(self):
#         return (self.user.first_name || self.user.last_name) ? self.user.first_name + " " + self.user.last_name : self.user.email

class Volunteer(models.Model):
    user = models.OneToOneField(User)
    trained = models.BooleanField(default=False)
    clients = models.ManyToManyField('Client', related_name='volunteers')

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name if (self.user.first_name or self.user.last_name) else self.user.email

class Client(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name if (self.user.first_name or self.user.last_name) else self.user.email

class ClientOpening(models.Model):
    client = models.ForeignKey(Client, db_column='clientId')
    startDate = models.DateTimeField('Start Date')
    endDate = models.DateTimeField('End Date')
    type = models.CharField(max_length=20)
    notes = models.CharField(max_length=255)

    def __unicode__(self):
        return "Client %d, Type %s, Start: %s" % (self.clientId, self.type, self.startDate)


class ClientOpeningMetadata(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    metadata = models.CharField(max_length=20)

    def __unicode__(self):
        return "Client opening %s, %s " % (self.clientOpening, self.metadata)


class ClientOpeningException(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    date = models.DateTimeField('Exception Date')

    def __unicode__(self):
        return "Client opening %s, %s " % (self.clientOpening, self.date)


class VolunteerCommitment(models.Model):
    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    volunteer = models.ForeignKey(Volunteer, db_column='volunteerId')
    startDate = models.DateTimeField('Start Date')
    endDate = models.DateTimeField('End Date')
    type = models.CharField(max_length=20)
    notes = models.CharField(max_length=255)

    def __unicode__(self):
        return "Volunteer %d, Type %s, Start: %s" % (self.volunteerId, self.type, self.startDate)


class VolunteerCommitmentMetadata(models.Model):
    volunteerCommitment = models.ForeignKey(VolunteerCommitment, db_column='volunteerCommitmentId')
    metadata = models.CharField(max_length=20)

    def __unicode__(self):
        return "Volunteer Commitment %s, %s " % (self.volunteerCommitment, self.metadata)


class ClientCommitmentException(models.Model):
    volunteerCommitment = models.ForeignKey(VolunteerCommitment, db_column='volunteerCommitmentId')
    date = models.DateTimeField('Exception Date')

    def __unicode__(self):
        return "Volunteer Commitment %s, %s " % (self.volunteerCommitment, self.date)




