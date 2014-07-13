from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'temp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/', include('appointments.apps.timeslots.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^', include('appointments.apps.common.urls')),
)
