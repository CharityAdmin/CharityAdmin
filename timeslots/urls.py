from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'paws.views.home', name='home'),
    # url(r'^paws/', include('paws.foo.urls')),

    url(r'^$', 'timeslots.views.home', name='timeslots_home'),
    # url(r'^$', 'timeslots.views.view_clientopening', name='timeslots_view_clientopening'),
)
