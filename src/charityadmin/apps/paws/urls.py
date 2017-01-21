from django.conf import settings
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from charityadmin.apps.timeslots import urls as timeslots_urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'paws.views.home', name='home'),
    # url(r'^paws/', include('paws.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^', include(timeslots_urls)),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'paws/login.html'}, name='paws_login'),
    url(r'^logout/$', 'charityadmin.apps.paws.views.logout_view', name='paws_logout'),
)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
