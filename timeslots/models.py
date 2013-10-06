from django.db import models


class ClientOpening(models.Model):
    def __unicode__(self):
        return "Client %d, Type %s, Start: %s" % (self.clientId, self.type, self.startDate)

    clientId = models.IntegerField()
    startDate = models.DateTimeField('Start Date')
    endDate = models.DateTimeField('End Date')
    type = models.CharField(max_length=20)
    notes = models.CharField(max_length=255)


class ClientOpeningMetadata(models.Model):
    def __unicode__(self):
        return "Client opening %s, %s " % (self.clientOpening, self.metadata)

    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    metadata = models.CharField(max_length=20)


class ClientOpeningException(models.Model):
    def __unicode__(self):
        return "Client opening %s, %s " % (self.clientOpening, self.date)

    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    date = models.DateTimeField('Exception Date')


class VolunteerCommitment(models.Model):
    def __unicode__(self):
        return "Volunteer %d, Type %s, Start: %s" % (self.volunteerId, self.type, self.startDate)

    clientOpening = models.ForeignKey(ClientOpening, db_column='clientOpeningId')
    volunteerId = models.IntegerField()
    startDate = models.DateTimeField('Start Date')
    endDate = models.DateTimeField('End Date')
    type = models.CharField(max_length=20)
    notes = models.CharField(max_length=255)


class VolunteerCommitmentMetadata(models.Model):
    def __unicode__(self):
        return "Client opening %s, %s " % (self.clientOpening, self.metadata)

    volunteerCommitment = models.ForeignKey(VolunteerCommitment, db_column='volunteerCommitmentId')
    metadata = models.CharField(max_length=20)


class ClientCommitmentException(models.Model):
    def __unicode__(self):
        return "Client opening %s, %s " % (self.clientOpening, self.date)

    volunteerCommitment = models.ForeignKey(VolunteerCommitment, db_column='volunteerCommitmentId')
    date = models.DateTimeField('Exception Date')