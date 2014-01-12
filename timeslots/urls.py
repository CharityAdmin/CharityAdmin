from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'paws.views.home', name='home'),
    # url(r'^paws/', include('paws.foo.urls')),

    url(r'^$', 'timeslots.views.home', name='timeslots_home'),
    url(r'^dashboard/$', 'timeslots.views.dashboard', name='timeslots_dashboard'),
    url(r'^user/add/$', 'timeslots.views.user_add', name='timeslots_user_add'),

    url(r'^clients/$', 'timeslots.views.clients_view', name='timeslots_clients_view'),
    url(r'^client/(?P<userid>\d+)/$', 'timeslots.views.client_view', name='timeslots_client_view'),
    url(r'^client/(?P<userid>\d+)/edit/$', 'timeslots.views.client_edit', name='timeslots_client_edit'),
    url(r'^client/(?P<userid>\d+)/edit/success/$', 'timeslots.views.client_edit_success', name='timeslots_client_edit_success'),

    url(r'^volunteers/$', 'timeslots.views.volunteers_view', name='timeslots_volunteers_view'),
    url(r'^volunteer/(?P<userid>\d+)/$', 'timeslots.views.volunteer_view', name='timeslots_volunteer_view'),
    url(r'^volunteer/(?P<userid>\d+)/edit/$', 'timeslots.views.volunteer_edit', name='timeslots_volunteer_edit'),
    url(r'^volunteer/(?P<userid>\d+)/edit/success/$', 'timeslots.views.volunteer_edit_success', name='timeslots_volunteer_edit_success'),

    url(r'^openings/$', 'timeslots.views.opening_instances_view', name='timeslots_openings_view'),
    url(r'^client/(?P<clientid>\d+)/openings/$', 'timeslots.views.opening_instances_view', name='timeslots_openings_view'),
    url(r'^client/(?P<clientid>\d+)/opening/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<time>\d+)$', 'timeslots.views.opening_instance_view', name='timeslots_opening_instance_view'),
    url(r'^opening/add/(?P<clientid>\d+)/$', 'timeslots.views.opening_add', name='timeslots_opening_add'),
    url(r'^opening/(?P<openingid>\d+)/$', 'timeslots.views.opening_pattern_view', name='timeslots_opening_view'),
    url(r'^opening/(?P<openingid>\d+)/edit/$', 'timeslots.views.opening_edit', name='timeslots_opening_edit'),
    url(r'^opening/(?P<openingid>\d+)/edit/success/$', 'timeslots.views.opening_edit_success', name='timeslots_opening_edit_success'),

    url(r'^scheduledvisits/$', 'timeslots.views.commitment_instances_view', name='timeslots_commitments_view'),
    url(r'^scheduledvisitpatterns/$', 'timeslots.views.commitment_patterns_view', name='timeslots_commitment_patterns_view'),
    url(r'^client/(?P<clientid>\d+)/scheduledvisits/$', 'timeslots.views.commitment_instances_view', name='timeslots_commitments_view'),
    url(r'^client/(?P<clientid>\d+)/scheduledvisit/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<time>\d+)$', 'timeslots.views.commitment_instance_view', name='timeslots_commitment_instance_view'),
    url(r'^scheduledvisit/add/(?P<openingid>\d+)/$', 'timeslots.views.commitment_add', name='timeslots_commitment_add'),
    url(r'^scheduledvisit/add/(?P<openingid>\d+)/v/(?P<volunteerid>\d+)$', 'timeslots.views.commitment_add', name='timeslots_commitment_add'),
    url(r'^scheduledvisit/(?P<commitmentid>\d+)/$', 'timeslots.views.commitment_pattern_view', name='timeslots_commitment_view'),
    url(r'^scheduledvisit/(?P<commitmentid>\d+)/edit/$', 'timeslots.views.commitment_edit', name='timeslots_commitment_edit'),
    url(r'^scheduledvisit/(?P<commitmentid>\d+)/edit/success/$', 'timeslots.views.commitment_edit_success', name='timeslots_commitment_edit_success'),

)
