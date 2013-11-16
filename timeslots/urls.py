from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'paws.views.home', name='home'),
    # url(r'^paws/', include('paws.foo.urls')),

    url(r'^$', 'timeslots.views.home', name='timeslots_home'),
    url(r'^dashboard/$', 'timeslots.views.volunteer_dashboard', name='timeslots_volunteer_dashboard'),
    url(r'^upcoming-commitments/$', 'timeslots.views.upcoming_commitments', name='timeslots_upcoming_commitments'),
    url(r'^upcoming-openings/$', 'timeslots.views.upcoming_openings', name='timeslots_upcoming_openings'),
    url(r'^client/(?P<clientname>\w+)$', 'timeslots.views.client_view', name='timeslots_client_view'),
    # url(r'^$', 'timeslots.views.view_clientopening', name='timeslots_view_clientopening'),
)
