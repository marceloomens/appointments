from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView

from .views import book, cancel, confirm, reminder

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'temp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(pattern_name='book'), name='home'),
    url(r'^book/$', book, name='book'),
    # What is the correct regular expression
    url(r'^cancel/(?P<payload>[.\w-]+)/$', cancel, name='cancel'),
    url(r'^confirm/(?P<payload>[.\w-]+)/$', confirm, name='confirm'),
    url(r'^finish/$', TemplateView.as_view(template_name='finish.html'), name='finish'),
    url(r'^reminder/$', reminder, name='reminder'),
)