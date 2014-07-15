from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from .views import book, cancel, confirm, reminder

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'temp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', book, name='home'),
    url(r'^cancel/$', cancel, name='cancel'),
    url(r'^confirm/$', confirm, name='confirm'),
    url(r'^finish/$', TemplateView.as_view(template_name='finish.html'), name='finish'),
    url(r'^reminder/$', reminder, name='reminder'),
)