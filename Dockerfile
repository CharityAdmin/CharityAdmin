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
    mkdir -p /srv/paws/{src,logs,static} && chown -R webapp:webapp /srv/paws

USER webapp
WORKDIR /srv/paws/src

# Add requirements separately to make builds faster when requirements haven't changed
COPY requirements.txt requirements.txt
# Install Python requirements
RUN pip install --user -r requirements.txt uwsgi==2.0.13

# Expose ports for HTTP and uWSGI stats
EXPOSE 8080 1717
VOLUME /srv/paws/logs

# Clean up APT when done.
USER root
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#CMD ["uwsgi", "--ini", "uwsgi.ini"]

#RUN mkdir /etc/service/uwsgi
#ADD uwsgi.sh /etc/service/uwsgi/run
