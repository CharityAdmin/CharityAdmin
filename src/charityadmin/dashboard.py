from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name

from lighthouse.apps.core.models import (
    VirtualMachine,
    Service,
    VirtualHost,
    Project,
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
            _('Manage Topology'),
            column=2,
            children = [
                modules.ModelList(
                    _('VMs, services, virtual hosts, projects ...'),
                    column=2,
                    models=('lighthouse.apps.core.models.*',),
                ),
            ]
        ))

        for vm in VirtualMachine.objects.all():
            vm_links =  ()
            vm_links += ({
                'title': vm.hostname,
                'url': '/',
                'external': False,
                'description': 'description',
            },)
            self.children.append(modules.Group(
                vm.hostname,
                column=2,
                children = [
                    modules.LinkList(
                        _("VMs"),
                        collapsible=True,
                        css_classes=('collapse closed',),
                        layout='inline',
                        column=1,
                        children=vm_links,
                    ),
                ]
            ))

