from django.conf import settings
from django.utils.translation import ugettext as _

from datetime import datetime, timedelta

from .signals import willEvaluateAvailabilityForRange as rangeSignal


def strfdate(date):
    return date.strftime(settings.TIMESLOTS_DATE_FORMAT)

def strftime(time):
    return time.strftime(settings.TIMESLOTS_TIME_FORMAT)

def strpdate(date):
    return datetime.strptime(date, settings.TIMESLOTS_DATE_FORMAT).date()   

def strptime(time):
    return datetime.strptime(time, settings.TIMESLOTS_TIME_FORMAT).time()



def __get_timeslots(date, definition):
    # Return timeslots for date given definition
    # Implement a caching strategy (map definition to parsed data)
    if date < definition.valid:
        raise ValueError('out of bounds')
    if definition.until and date > definition.until:
        raise ValueError('out of bounds')
        
    WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday']
    defaults = definition.json.get('defaults', None)
    timeslots = {
                weekday: { strptime(t): a for (t, a) in definition.json.get(weekday, defaults).items() }
                if definition.json.get(weekday, defaults)
                else []
            for weekday in WEEKDAYS
        }

    from copy import copy
    return copy(timeslots[WEEKDAYS[date.weekday()]])
    
def __timeslots_generator(lbound, ubound, constraint):
    
    definitions = constraint.definitions.filter(enabled=True)
    
    # Select all definitions in the date rage
    future_set = definitions.filter(valid__range=(lbound, ubound))
    current = definitions.filter(valid__lt=lbound).order_by('-valid')[:1]

    # Union of the current definition and all future definitions in the date
    # range. The union operator | may set me up for all sorts of associativity
    # problems. writing (current | future_set) throws AssertionError: Cannot
    # combine queries once a slice has been taken
    
    # There's no risk of getting duplicate rows, so I should be able to drop the
    # call to distinct('id'). only PostgreSQL supports DISTINCT ON

    # definitions = (future_set | current).distinct('id').order_by('valid')
    definitions = (future_set | current).order_by('valid')
    
    # Raise warnings if definitions is over- or underspecified
    
    def timeslots(date):
        final = None
        for definition in definitions:
            if definition.valid <= date:
                final = definition
            else:
                break
        return __get_timeslots(date, final) if final else None
        
    return timeslots
    
def availability(lbound, ubound, constraint):
    # I can load the entire queryset in one fould sweep here...
    generator = __timeslots_generator(lbound, ubound, constraint)
    
    # Take note of holidays
    holidays = constraint.holidays.filter(date__range=(lbound, ubound))

    # Allow signal listeners to register callback function
    callbacks = rangeSignal.send(__name__, lbound=lbound, ubound=ubound, constraint=constraint)
    
    for n in range((ubound-lbound).days):
        date = lbound + timedelta(n)
        # If date is a holiday, bail here
        
        if holidays.filter(date=date).count() > 0:
            data = {
                    'available' : False,
                    'status'    : 'holiday',
                    'code'      : 3,
                     # Replace with holiday message
                    'msg'       : _("holiday"),
                    'timeslots' : [],
                }
            
        else:
            timeslots = generator(date)
            if timeslots:
                # Allow signal handlers to update timeslots            
                for (receiver, callback) in callbacks:
                    try: 
                        callback(date, timeslots)
                    except Exception as e:
                        import logging
                        l = logging.getLogger(__name__)
                        l.warning("willEvaluateAvailabilityForRange callback threw an exception.", extra=e)
                # If final is empty then the date is fully booked...
                final = [strftime(k) for (k, v) in timeslots.items() if v > 0]
                data =  {
                    'available' : True if final else False,
                    'status'    : 'available' if final else 'fully booked',
                    'code'      : 0 if final else 2,
                    'msg'       : _("available") if final else _("fully booked"), 
                    'timeslots' : final,
                }
    
            else:
                data =  {
                    'available' : False,
                    'status'    : 'unavailable',
                    'code'      : 1,
                    'msg'       : _("unavailable"), 
                    'timeslots' : [],
                }

        yield date, data  