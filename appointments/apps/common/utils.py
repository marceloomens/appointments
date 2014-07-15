from django.conf import settings
from django.dispatch import receiver

from itsdangerous import URLSafeSerializer

from appointments.apps.timeslots.signals import willEvaluateAvailabilityForRange

from .models import Appointment

def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = settings.config['SECRET_KEY']
    return URLSafeSerializer(secret_key)
    

@receiver(willEvaluateAvailabilityForRange)
def availability_for_range_handler(sender, **kwargs):
    
    # Preventing sorting should speed up my query
    # Sorting the queryset may enable some clever
    # heuristics in my subsequent loops
    appointments = Appointment.objects.filter(constraint=kwargs['constraint'],
        date__range=(kwargs['lbound'], kwargs['ubound']))
                
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