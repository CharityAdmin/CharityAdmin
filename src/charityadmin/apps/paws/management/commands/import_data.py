import faker
import json
#import csv
import os.path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from charityadmin.apps.timeslots.models import Client


"""
{u'Active_Jobs': 0,
 u'Active_Visits_Week': 0,
 u'Address': u'120 W. 91st St., Apt #8L',
 u'Age': 67.17,
 u'Approval_Status': u'',
 u'Auto_Number': 531,
 u'Barrier': u'',
 u'Borough': u'',
 u'CMOW': False,
 u'Cats': u'',
 u'City': u'',
 u'Date_of_Application': u'',
 u'Date_of_Phone_Intake': u'2016-06-13',
 u'Deceased': False,
 u'Description_of_Need': u'',
 u'DoB': u'1949-04-30',
 u'Dogs': 1,
 u'Email_Address': u'',
 u'Emergency_Contact_Information': u'',
 u'First_Name': u'Patricia',
 u'Full_Name': u'Patricia Valadez',
 u'HIV_AIDS': [],
 u'Ideal_Weekly_Visits': u'',
 u'Info_Details': u'',
 u'JASA': False,
 u'Last_Name': u'Valadez',
 u'MedicAlert': False,
 u'Monthly_Income': u'',
 u'Needs': [u'Dog Walking'],
 u'Other_Info': u'',
 u'Other_Pets': u'',
 u'Pet_Food': [],
 u'Pet_Food_If_Brand_Not_Listed_Above': u'',
 u'Pet_Name_type': u'',
 u'Phone': u'347-376-0778',
 u'Referring_Org': u'',
 u'Social_Worker_Case_Manager': u'',
 u'Total_Pets': u'',
 u'Waitlist': False,
 u'Zip_Code': u'10024'}
"""

def gen_email():
    fk = faker.Faker()
    return fk.email()


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        with open("/home/pk/Documents/Clients/PawsNYC/Clients_View.json") as f:
            for client in json.loads(f.read())['Clients']:
                if not client.get('Last_Name'):
                    print "no data"
                    print client
                    print "/no data"
                    continue
                u, created = User.objects.get_or_create(
                    first_name=client.get('First_Name'),
                    last_name=client.get('Last_Name'),
                    username="_".\
                        join([
                            client.get('First_Name'), 
                            client.get('Last_Name')])[:20]
                    #defaults={'email': client.get('Email_Address', gen_email())}
                )
                if not u.email:
                    u.email = gen_email()
                    u.save()

                if created:
                    print "created user", u.first_name, u.last_name, u.email
                    u.set_unusable_password()
                    u.save()

                c, created = Client.objects.get_or_create(
                        user=u,
                        address=client.get('Address'),
                        phone=client.get('Phone').replace('-', ''),
                        zipcode=client.get('Zip_Code'),
                        city=client.get('City'),
                )
                if created:
                    print "created client", c


