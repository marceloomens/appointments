from django.conf import settings
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import ugettext as _

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

def send_confirmation(request, appointment):
    t = get_template('email/confirmation.txt')
    # h = get_template('email/confirmation.html')
    c = Context({'appointment': appointment,})
    payload = {
            'to'        : appointment.user.email,
            'subject'   : _("Appointment confirmation"),
            'text_body' : t.render(c),
            # 'html_body' : h.render(c),
        }
    send_mail.delay(**payload) if getattr(settings, 'SEND_MAIL_ASYNC', False) else send_mail(**payload)

def send_receipt(appointment):
    t = get_template('email/receipt.txt')
    # h = get_template('email/receipt.html')
    c = Context({'appointment': appointment,})
    payload = {
            'to'        : appointment.user.email,
            'subject'   : _("Please confirm your appointment"),
            'text_body' : t.render(c),
            # 'html_body' : h.render(c),
        }
    send_mail.delay(**payload) if getattr(settings, 'SEND_MAIL_ASYNC', False) else send_mail(**payload)

def send_reminder(user, appointments):
    t = get_template('email/reminder.txt')
    # h = get_template('email/reminder.html')
    c = Context({'appointments': appointments})
    payload = {
            'to'        : user.email,
            'subject'   : _("Reminder of your appointments"),
            'text_body' : t.render(c),
            # 'html_body'  : h.render(c),
        }
    send_mail.delay(**payload) if getattr(settings, 'SEND_MAIL_ASYNC', False) else send_mail(**payload)

def send_report(report, appointments=None):
    # If appointments = None then generate today's report
    if not appointments:
        date = timezone.now().date()
        appointments = Appointment.objects.filter(constraint=report.constraint, date=date).order_by('time')
    t = get_template('email/report.txt')
    h = get_template('email/report.html')
    c = Context({'report': report, 'appointments': appointments,})
    payload = {
            'to'        : report.user.email,
            'subject'   : _("Report of appointments"),
            'text_body' : t.render(c),
            'html_body' : h.render(c),
        }
    send_mail.delay(**payload) if getattr(settings, 'SEND_MAIL_ASYNC', False) else send_mail(**payload)