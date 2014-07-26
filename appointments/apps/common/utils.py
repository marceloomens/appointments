from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import ugettext as _

from urlparse import urlunsplit
from itsdangerous import URLSafeSerializer

from appointments.apps.timeslots.signals import willEvaluateAvailabilityForRange

from .models import Appointment
from .tasks import send_mail


@receiver(willEvaluateAvailabilityForRange)
def availability_for_range_handler(sender, **kwargs):
    
    # Ignore cancelled appointments...
    appointments = Appointment.objects.filter(constraint=kwargs['constraint'],
        date__range=(kwargs['lbound'], kwargs['ubound']))
    appointments = appointments.exclude(status='CA')
                
    def availability_for_date_callback(date, timeslots):
    
        for appointment in appointments:
            if date == appointment.date:
                if appointment.time in timeslots:
                    timeslots[appointment.time] -= 1
                else:
                    # Throw a warning, this should never happen after all...
                    import logging
                    l = logging.getLogger(__name__)
                    l.warning("Encountered booking for non-existing timeslot.", extra={'appointment_id': appointment.pk})
                    
    return availability_for_date_callback
    
    
def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = settings.SECRET_KEY
    return URLSafeSerializer(secret_key)

### SENDING EMAIL ###

def __parse_request(request):
    scheme = 'https' if request.is_secure() else 'http'
    # Use the Sites framework to obtain the host
    site = Site.objects.get(pk=settings.SITE_ID)
    host = site.domain
    return (scheme, host)

def send_confirmation(request, appointment):
    pass

def send_receipt(request, appointment):
    scheme, host = __parse_request(request)
    urls = {
            'confirm': urlunsplit([scheme, host, reverse('confirm', kwargs={'payload': appointment.get_url_safe_key()}),'','']),
            'cancel' : urlunsplit([scheme, host, reverse('cancel', kwargs={'payload': appointment.get_url_safe_key()}),'','']),
        }
    t = get_template('email/receipt.txt')
    c = Context({'appointment': appointment, 'urls': urls})
    payload = {
            'to'        : appointment.user.email,
            'subject'   : _("Please confirm your appointment"),
            'text_body' : t.render(c),
            # 'html_body' : h.render(c),
        }
    send_mail.delay(**payload) if getattr(settings, 'SEND_MAIL_ASYNC', False) else send_mail(**payload)
    
def send_report(request, report, appointments=None):
    # If appointments = None then generate today's report
    if not appointments:
        date = timezone.now().date()
        appointments = Appointment.objects.filter(constraint=report.constraint, date=date).order_by('time')
    t = get_template('email/report.txt')
    h = get_template('email/report.html')
    c = Context({'report': report, 'appointments': appointments})
    payload = {
            'to'        : report.user.email,
            'subject'   : _("Report of appointments"),
            'text_body' : t.render(c),
            'html_body' : h.render(c),
        }
    send_mail.delay(**payload) if getattr(settings, 'SEND_MAIL_ASYNC', False) else send_mail(**payload)