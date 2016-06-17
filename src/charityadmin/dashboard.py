from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name

from charityadmin.apps.timeslots.models import (
    Volunteer,
    Client,
    ClientOpening,
    VolunteerCommitment,
)

import logging
log = logging.getLogger(__name__)


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        req = context.get('request')

        self.children.append(modules.Group(
            _('Manage Volunteers and Clients'),
            column=2,
            children = [
                modules.ModelList(
                    _('Volunteers and Clients'),
                    column=2,
                    models=('charityadmin.apps.timeslots.models.*',),
                ),
            ]
        ))


