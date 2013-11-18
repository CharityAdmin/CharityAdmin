"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime
from datetime import tzinfo
from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from timeslots.models import Client, ClientOpening, ClientOpeningException, ClientOpeningMetadata, Volunteer, VolunteerCommitment, VolunteerCommitmentException, VolunteerCommitmentMetadata


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ClientOpeningInstances_DaysOfWeek_TestCase(TestCase):
	def setUp(self):
		# Basic set up
		now = timezone.now()
		self.clientUser = User.objects.create(username='ClientUser')
		self.client = Client.objects.create(user=self.clientUser)
		self.volunteerUser = User.objects.create(username='VolunteerUser')
		self.volunteer = Volunteer.objects.create(user=self.volunteerUser)

		# Days of Week Client Openings All Prep
		self.clientOpening_daysOfWeek = ClientOpening.objects.create(client=self.client, type="Days of Week", startDate=now, endDate=now + datetime.timedelta(days=7))
		self.clientOpeningMetaData_daysOfWeek_M = ClientOpeningMetadata.objects.create(clientOpening=self.clientOpening_daysOfWeek, metadata="M")
		self.clientOpeningMetaData_daysOfWeek_Tu = ClientOpeningMetadata.objects.create(clientOpening=self.clientOpening_daysOfWeek, metadata="Tu")
		self.clientOpeningMetaData_daysOfWeek_F = ClientOpeningMetadata.objects.create(clientOpening=self.clientOpening_daysOfWeek, metadata="F")

		# Days of Week Client Openings Filled Prep
		self.volunteerCommitment_daysOfWeek = VolunteerCommitment.objects.create(volunteer=self.volunteer, clientOpening=self.clientOpening_daysOfWeek, type="Days of Week", startDate=now, endDate=now + datetime.timedelta(days=7))
		self.volunteerCommitmentMetaData_daysOfWeek_M = VolunteerCommitmentMetadata.objects.create(volunteerCommitment=self.volunteerCommitment_daysOfWeek, metadata="M")
		self.volunteerCommitmentMetaData_daysOfWeek_F = VolunteerCommitmentMetadata.objects.create(volunteerCommitment=self.volunteerCommitment_daysOfWeek, metadata="F")

	def tearDown(self):
		self.clientUser.delete()
		self.client.delete()
		self.volunteerUser.delete()
		self.volunteer.delete()

		self.clientOpening_daysOfWeek.delete()
		self.clientOpeningMetaData_daysOfWeek_M.delete()
		self.clientOpeningMetaData_daysOfWeek_Tu.delete()
		self.clientOpeningMetaData_daysOfWeek_F.delete()

		self.volunteerCommitment_daysOfWeek.delete()
		self.volunteerCommitmentMetaData_daysOfWeek_M.delete()
		self.volunteerCommitmentMetaData_daysOfWeek_F.delete()

	def test_ClientOpeningGetInstancesMethod_Should_Return_Correct_DaysOfWeek(self):
		"""
		Tests that ClientOpening.get_instances() returns instances specified by the metadata
		"""
		clientUser = User.objects.get(username='ClientUser')
		opening = clientUser.client.openings.all()[0]
		instances = opening.get_instances()
		self.assertEqual(set([instance['date'].strftime("%A") for instance in instances]), set(['Monday', 'Tuesday', 'Friday']))

	def test_ClientOpeningGetFilledInstancesMethod_Should_Return_Correct_DaysOfWeek(self):
		"""
		Tests that ClientOpening.get_instances() returns instances specified by the metadata
		"""
		clientUser = User.objects.get(username='ClientUser')
		opening = clientUser.client.openings.all()[0]
		instances = opening.get_filled_instances(startDate=timezone.now())
		self.assertEqual(set([instance['date'].strftime("%A") for instance in instances]), set(['Monday', 'Friday']))

	def test_ClientOpeningGetUnfilledInstancesMethod_Should_Return_Correct_DaysOfWeek(self):
		"""
		Tests that ClientOpening.get_instances() returns instances specified by the metadata
		"""
		clientUser = User.objects.get(username='ClientUser')
		opening = clientUser.client.openings.all()[0]
		instances = opening.get_unfilled_instances(startDate=timezone.now())
		self.assertEqual(set([instance['date'].strftime("%A") for instance in instances]), set(['Tuesday']))


