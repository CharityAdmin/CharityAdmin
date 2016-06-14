#!/bin/sh

# `/sbin/setuser webapp` runs the given command as the user `webapp`.
# If you omit that part, the command will be run as root.
exec /sbin/setuser webapp /usr/local/bin/uwsgi --ini  /srv/paws/src/uwsgi.ini
