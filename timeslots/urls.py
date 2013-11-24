from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'paws.views.home', name='home'),
    # url(r'^paws/', include('paws.foo.urls')),

    url(r'^$', 'timeslots.views.home', name='timeslots_home'),
    url(r'^dashboard/$', 'timeslots.views.volunteer_dashboard', name='timeslots_volunteer_dashboard'),

    url(r'^commitments/$', 'timeslots.views.commitments_view', name='timeslots_commitments_view'),
    url(r'^commitment/add/(?P<openingid>\w+)/$', 'timeslots.views.commitment_add', name='timeslots_commitment_add'),
    url(r'^commitment/add/(?P<openingid>\w+)/v/(?P<volunteerid>\w+)$', 'timeslots.views.commitment_add', name='timeslots_commitment_add'),
    url(r'^commitment/(?P<commitmentid>\w+)/$', 'timeslots.views.commitment_view', name='timeslots_commitment_view'),
    url(r'^commitment/(?P<commitmentid>\w+)/edit/$', 'timeslots.views.commitment_edit', name='timeslots_commitment_edit'),
    url(r'^commitment/(?P<commitmentid>\w+)/edit/success/$', 'timeslots.views.commitment_edit_success', name='timeslots_commitment_edit_success'),

    url(r'^openings/$', 'timeslots.views.openings_view', name='timeslots_openings_view'),
    url(r'^opening/add/(?P<clientid>\w+)/$', 'timeslots.views.opening_add', name='timeslots_opening_add'),
    url(r'^opening/add/(?P<clientid>\w+)/v/(?P<volunteerid>\w+)$', 'timeslots.views.opening_add', name='timeslots_opening_add'),
    url(r'^opening/(?P<openingid>\w+)/$', 'timeslots.views.opening_view', name='timeslots_opening_view'),
    url(r'^opening/(?P<openingid>\w+)/edit/$', 'timeslots.views.opening_edit', name='timeslots_opening_edit'),
    url(r'^opening/(?P<openingid>\w+)/edit/success/$', 'timeslots.views.opening_edit_success', name='timeslots_opening_edit_success'),

    url(r'^user/add/$', 'timeslots.views.user_add', name='timeslots_user_add'),

    url(r'^clients/$', 'timeslots.views.clients_view', name='timeslots_clients_view'),
    url(r'^client/(?P<userid>\w+)/$', 'timeslots.views.client_view', name='timeslots_client_view'),
    url(r'^client/(?P<userid>\w+)/edit/$', 'timeslots.views.client_edit', name='timeslots_client_edit'),
    url(r'^client/(?P<userid>\w+)/edit/success/$', 'timeslots.views.client_edit_success', name='timeslots_client_edit_success'),

    url(r'^volunteers/$', 'timeslots.views.volunteers_view', name='timeslots_volunteers_view'),
    url(r'^volunteer/(?P<userid>\w+)/$', 'timeslots.views.volunteer_view', name='timeslots_volunteer_view'),
    url(r'^volunteer/(?P<userid>\w+)/edit/$', 'timeslots.views.volunteer_edit', name='timeslots_volunteer_edit'),
    url(r'^volunteer/(?P<userid>\w+)/edit/success/$', 'timeslots.views.volunteer_edit_success', name='timeslots_volunteer_edit_success'),


)
