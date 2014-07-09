from django.conf.urls import patterns, include, url

from .views import countries, locations, timeslots, ng_test

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'temp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^countries/$', countries, name='counties_api'),
    # I can probably improve on those regular expressions
    url(r'^locations/(?P<country>[\d\D]+)/$', locations, name='locations_api'),
    url(r'^timeslots/(?P<location>[\d\D]+)/$', timeslots, name='timeslots_api'),
    
    url(r'^ng-test/$', ng_test, name='ng-test'),
)
