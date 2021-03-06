from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import ugettext as _

from itsdangerous import URLSafeSerializer

import logging

from appointments.apps.timeslots.signals import willEvaluateAvailabilityForRange

from .models import Appointment
from .tasks import send_mail


class DjangoRequestLoggerAdapter (logging.LoggerAdapter):

    def process(self, msg, kwargs):
        return "[%s %s] %s" % (self.extra.method, self.extra.path, msg), kwargs


class EmailAuthenticationBackend (ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            email = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get(email__iexact=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)


@receiver(willEvaluateAvailabilityForRange)
def availability_for_range_handler(sender, **kwargs):
    
    # Ignore cancelled appointments...
    appointments = Appointment.objects.filter(constraint=kwargs['constraint'],
        date__range=(kwargs['lbound'], kwargs['ubound']))
    appointments = appointments.exclude(status='CA')
                
    def availability_for_date_callback(date, timeslots, supress_warnings=False):
    
        for appointment in appointments:
            if date == appointment.date:
                if appointment.time in timeslots:
                    timeslots[appointment.time] -= 1
                elif not supress_warnings:
                    # Throw a warning, this should never happen after all,
                    # but might happen when called from is_available
                    import logging
                    l = logging.getLogger(__name__)
                    l.warning("Encountered booking for non-existing timeslot.", extra={'appointment_id': appointment.pk})
                else:
                    pass
                    
    return availability_for_date_callback
    

def get_logger(name=None, request=None, *args, **kwargs):
    logger = logging.getLogger(name, *args, **kwargs)
    return DjangoRequestLoggerAdapter(logger, request)

def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = settings.SECRET_KEY
    return URLSafeSerializer(secret_key)

### SENDING EMAIL ###

def send_confirmation(appointment):
    t = get_template('email/confirmation.txt')
    # h = get_template('email/confirmation.html')
    c = Context({'appointment': appointment,})
    payload = {
            'from_name' : 'Consular representation in %s' % (appointment.constraint.name),
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
            'from_name' : 'Consular representation in %s' % (appointment.constraint.name),
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

def send_report(report, appointments):
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