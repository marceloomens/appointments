from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from urlparse import urlunsplit

from ..models import Appointment

register = template.Library()

site = Site.objects.get(pk=settings.SITE_ID)
scheme = 'https' if getattr(settings, 'HTTPS', False) else 'http'
host = site.domain

@register.filter(name='absurl')
def abs_url(url_name):
    return urlunsplit([scheme, host, reverse(url_name),'',''])

@register.filter(name='cancel')
def cancel_url(appointment):
    if not isinstance(appointment, Appointment):
        raise ValueError("Cancel requires an Appointment to cancel")
    return urlunsplit([scheme, host, reverse('cancel', kwargs={'payload': appointment.get_url_safe_key()}),'',''])

@register.filter(name='confirm')    
def confirm_url(appointment):
    if not isinstance(appointment, Appointment):
        raise ValueError("Confirm requires an Appointment to confirm")
    return urlunsplit([scheme, host, reverse('confirm', kwargs={'payload': appointment.get_url_safe_key()}),'',''])
    
@register.filter(name='changeform')
def model_change_form(model):
    if not isinstance(model, Appointment):
        raise ValueError("Changeform currently works for Appointment model only")
    return urlunsplit([scheme, host, reverse('admin:common_appointment_change', args=(model.pk,)),'',''])
    
@register.filter(name='prettystatus')
def pretty_status(key):
    values = {
            'CA' : 'cancelled',
            'CO' : 'confirmed',
            'PE' : 'pending'
        }
    return values.get(key)