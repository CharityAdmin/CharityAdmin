Linux Setup
=====

1. Install python 2.7.x
1. Install setup tools `sudo apt-get install python-setuptools`
1. Install pip `sudo apt-get install python-pip`
1. Install django `sudo pip install django==1.5.5`
1. Install git `sudo apt-get install git`
1. Install `pip install django-localflavor`
1. Clone this repository
1. `sudo apt-get update --fix-missing`
1. `sudo apt-get install libpq-dev python-dev`
1. `sudo pip install psycopg2`
1. `sudo pip install python-dateutil`
1. Build schema `python manage.py syncdb`
1. Run app `python manage.py runserver` 

Using Postgre
=====
1. Install postgres 9.3.1+, using full installer (not standaline app/exe)
1. Create empty paws db
1. `sudo pip install postgresql-devel`
1. `sudo pip install psycopg2`
1. Build schema `python manage.py syncdb`
  1. Setup credentials and update settings.py accordingly (name, username, password) 
