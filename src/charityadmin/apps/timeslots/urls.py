from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'paws.views.home', name='home'),
    # url(r'^paws/', include('paws.foo.urls')),

    # General
    url(r'^$', 'charityadmin.apps.timeslots.views.home', name='timeslots_home'),
    url(r'^dashboard/$', 'charityadmin.apps.timeslots.views.dashboard', name='timeslots_dashboard'),
    url(r'^user/add/$', 'charityadmin.apps.timeslots.views.user_add', name='timeslots_user_add'),
    url(r'^signup/$', 'charityadmin.apps.timeslots.views.volunteer_signup', name='timeslots_volunteer_signup'),
    url(r'^signup/success$', 'charityadmin.apps.timeslots.views.volunteer_signup_success', name='timeslots_volunteer_signup_success'),

    # Client Create/Edit
    url(r'^clients/$', 'charityadmin.apps.timeslots.views.clients_view', name='timeslots_clients_view'),
    url(r'^client/(?P<userid>\d+)/$', 'charityadmin.apps.timeslots.views.client_view', name='timeslots_client_view'),
    url(r'^client/(?P<userid>\d+)/edit/$', 'charityadmin.apps.timeslots.views.client_edit', name='timeslots_client_edit'),
    url(r'^client/add/$', 'charityadmin.apps.timeslots.views.user_add', {'usertype': 'client'}, name='timeslots_client_add'),

    # Volunteer Create/Edit
    url(r'^volunteers/$', 'charityadmin.apps.timeslots.views.volunteers_view', name='timeslots_volunteers_view'),
    url(r'^volunteer/(?P<userid>\d+)/$', 'charityadmin.apps.timeslots.views.volunteer_view', name='timeslots_volunteer_view'),
    url(r'^volunteer/(?P<userid>\d+)/edit/$', 'charityadmin.apps.timeslots.views.volunteer_edit', name='timeslots_volunteer_edit'),
    url(r'^volunteer/add/$', 'charityadmin.apps.timeslots.views.user_add', {'usertype': 'volunteer'}, name='timeslots_volunteer_add'),

    # Opening Instances/Patterns View & Edit
    url(r'^openings/$', 'charityadmin.apps.timeslots.views.opening_instances_view', name='timeslots_openings_view'),
    url(r'^client/(?P<clientid>\d+)/openings/$', 'charityadmin.apps.timeslots.views.opening_instances_view', name='timeslots_openings_view'),
    url(r'^client/(?P<clientid>\d+)/openingpatterns/edit/$', 'charityadmin.apps.timeslots.views.opening_patterns_view', { 'editlinks': True }, name='timeslots_opening_patterns_edit'),
    url(r'^client/(?P<clientid>\d+)/opening/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<time>\d+)/$',
        'charityadmin.apps.timeslots.views.opening_instance_view', name='timeslots_opening_instance_view'),
    url(r'^opening/add/(?P<clientid>\d+)/$', 'charityadmin.apps.timeslots.views.opening_add', name='timeslots_opening_add'),
    url(r'^opening/(?P<openingid>\d+)/$', 'charityadmin.apps.timeslots.views.opening_pattern_view', name='timeslots_opening_view'),
    url(r'^opening/(?P<openingid>\d+)/edit/$', 'charityadmin.apps.timeslots.views.opening_edit', name='timeslots_opening_edit'),
    url(r'^opening/(?P<openingid>\d+)/exception/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<time>\d+)/$',
        'charityadmin.apps.timeslots.views.opening_exception_view', name='timeslots_opening_exception_view'),
    url(r'^opening/(?P<openingid>\d+)/exception/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<time>\d+)/delete/$',
        'charityadmin.apps.timeslots.views.opening_exception_delete', name='timeslots_opening_exception_delete'),

    # Commitments/Scheduled Visits Instances/Pattners View & Edit
    url(r'^scheduledvisits/$', 'charityadmin.apps.timeslots.views.commitment_instances_view', name='timeslots_commitments_view'),
    url(r'^scheduledvisitpatterns/$', 'charityadmin.apps.timeslots.views.commitment_patterns_view', name='timeslots_commitment_patterns_view'),
    url(r'^scheduledvisitpatterns/edit/$', 'charityadmin.apps.timeslots.views.commitment_patterns_view', { 'editlinks': True }, name='timeslots_commitment_patterns_edit'),
    url(r'^volunteer/(?P<volunteerid>\d+)/scheduledvisitpatterns/$', 'charityadmin.apps.timeslots.views.commitment_patterns_view', name='timeslots_commitment_patterns_view'),
    url(r'^volunteer/(?P<volunteerid>\d+)/scheduledvisitpatterns/edit/$',
        'charityadmin.apps.timeslots.views.commitment_patterns_view', { 'editlinks': True }, name='timeslots_commitment_patterns_edit'),
    url(r'^client/(?P<clientid>\d+)/scheduledvisitpatterns/edit/$', 'charityadmin.apps.timeslots.views.commitment_patterns_view', { 'editlinks': True }, name='timeslots_commitment_patterns_edit_client'),
    url(r'^client/(?P<clientid>\d+)/scheduledvisits/$', 'charityadmin.apps.timeslots.views.commitment_instances_view', name='timeslots_commitments_view'),
    url(r'^client/(?P<clientid>\d+)/scheduledvisit/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<time>\d+)$',
        'charityadmin.apps.timeslots.views.commitment_instance_view', name='timeslots_commitment_instance_view'),
    url(r'^scheduledvisit/add/(?P<openingid>\d+)/$', 'charityadmin.apps.timeslots.views.commitment_add', name='timeslots_commitment_add'),
    url(r'^scheduledvisit/add/v/(?P<volunteerid>\d+)/selectopening/$',
            'charityadmin.apps.timeslots.views.commitment_add_opening_select', name='timeslots_commitment_add_opening_select'),
    url(r'^scheduledvisit/add/(?P<openingid>\d+)/v/(?P<volunteerid>\d+)$',
            'charityadmin.apps.timeslots.views.commitment_add', name='timeslots_commitment_add'),
    url(r'^scheduledvisit/(?P<commitmentid>\d+)/$', 'charityadmin.apps.timeslots.views.commitment_pattern_view', name='timeslots_commitment_view'),
    url(r'^scheduledvisit/(?P<commitmentid>\d+)/edit/$', 'charityadmin.apps.timeslots.views.commitment_edit', name='timeslots_commitment_edit'),
    url(r'^scheduledvisit/(?P<commitmentid>\d+)/exception/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<time>\d+)/$',
            'charityadmin.apps.timeslots.views.commitment_exception_view', name='timeslots_commitment_exception_view'),
    url(r'^scheduledvisit/(?P<commitmentid>\d+)/exception/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<time>\d+)/delete/$',
            'charityadmin.apps.timeslots.views.commitment_exception_delete', name='timeslots_commitment_exception_delete'),
)
