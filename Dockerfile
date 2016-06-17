# Use phusion/baseimage as base image. To make your builds
# reproducible, make sure you lock down to a specific version, not
# to `latest`! See
# https://github.com/phusion/baseimage-docker/blob/master/Changelog.md
# for a list of version numbers.
FROM phusion/baseimage:0.9.18
MAINTAINER Philip Kalinsky <philip.kalinsky@eloquentbits.com>

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# ...put your own build instructions here...
# Set locale
RUN localedef -c -i en_US -f UTF-8 en_US.UTF-8
ENV LANG="en_US.UTF-8" LANGUAGE="en_US:en" LC_ALL="en_US.UTF-8"

RUN apt-get update && apt-get upgrade -y -o Dpkg::Options::="--force-confold"

RUN apt-get install -y \
    python-setuptools \
    build-essential \
    python-dev \
    openssl \
    libreadline6 libreadline6-dev \
    libxml2-dev libxslt-dev \
    libpq-dev \
    curl zlib1g zlib1g-dev libssl-dev && \
    easy_install pip

# http://blog.dscpl.com.au/2015/12/don-run-as-root-inside-of-docker.html
RUN groupadd -r webapp && useradd -r -g webapp -d /srv/paws webapp && \
    mkdir -p /srv/paws/{src,logs,static,uploads} && chown -R webapp:webapp /srv/paws

USER webapp
WORKDIR /srv/paws/src

# Add requirements separately to make builds faster when requirements haven't changed
COPY requirements.txt requirements.txt
# Install Python requirements
RUN pip install --user -r requirements.txt uwsgi==2.0.13

# Expose ports for HTTP and uWSGI stats
EXPOSE 8080 1717
VOLUME /srv/paws/logs

# Add source files to container with correct permissions
COPY . .
USER root
RUN chown -R webapp:webapp .
USER webapp

# Install Python project, link settings, build and collect staticfiles
RUN pip install --user -e . 
#python manage.py collectstatic --noinput
#python manage.py migrate --noinput 

USER root
COPY django-configurations django-configurations
WORKDIR /srv/paws/src/django-configurations
RUN pip install setuptools_git && python setup.py install

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /etc/service/uwsgi
ADD uwsgi.sh /etc/service/uwsgi/run

WORKDIR /srv/paws/src

#RUN chmod 755 /etc/container_environment && chmod 644 /etc/container_environment.sh
#/etc/container_environment.json && chmod 777 /etc/container_environment/*

