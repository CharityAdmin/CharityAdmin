from django.conf.urls import patterns, include, url
import timeslots

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

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
    url(r'^', include('timeslots.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'paws/login.html'}, name='paws_login'),
    url(r'^logout/$', 'paws.views.logout_view', name='paws_logout'),
)
