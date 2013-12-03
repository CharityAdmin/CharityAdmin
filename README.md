Setup
=====

1. Install python 2.7.x
1. Install mysql 5.5
1. Install django `pip install django`
1. Install `pip install django-localflavor`
1. Clone this repository
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
