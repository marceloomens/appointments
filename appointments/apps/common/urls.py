from django.conf.urls import patterns, include, url

from .views import book

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'temp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', book, name='home'),
)