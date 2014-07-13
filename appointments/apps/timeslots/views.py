from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_GET

from datetime import timedelta

import json

from .models import ConstraintSet, Constraint, Definition
from .utils import availability, strfdate, strpdate

# Create your views here.

def ng_test(request):
    return render(request, template_name='ng-test.html')

@require_GET
def actions(request, location):
    location = get_object_or_404(Constraint, slug=location)
    data = serializers.serialize('json', location.actions.all())
    return HttpResponse(data, content_type='application/json')

@require_GET
def countries(request):
    # Filter disables countries
    # data = [(country.name, country.slug) for country in ConstraintSet.objects.all()]
    # return HttpResponse(json.dumps(data), content_type='application/json')
    data = serializers.serialize('json', ConstraintSet.objects.all())
    return HttpResponse(data, content_type='application/json')


@require_GET
def locations(request, country):
    country = get_object_or_404(ConstraintSet, slug=country)
    # data = [(location.name, location.slug) for location in country.values.all()]
    # return HttpResponse(json.dumps(data), content_type='application/json')
    data = serializers.serialize('json', country.values.all())
    return HttpResponse(data, content_type='application/json')

@require_GET
def timeslots(request, location):
    location = get_object_or_404(Constraint, slug=location)

    # Defaults
    today = timezone.now().date()
    minbound = today + timedelta(1)
    maxbound = minbound + timedelta(settings.TIMESLOTS_FUTURE)

    # QueryDict object does not support pop/2
    qs = request.GET.dict()
    # Pop value or default to None
    date        = qs.pop('date', None)
    lbound      = qs.pop('lbound', None)
    ubound      = qs.pop('ubound', None)

    if date and lbound:
        return HttpResponseBadRequest()
    elif date and ubound:
        return HttpResponseBadRequest()
    elif date:
        # That's okay
        try:
            date = strpdate(date)
        except ValueError:
            return HttpResponseBadRequest()
            
        if date < minbound or maxbound < date:
            data = {
                    'error'     : 'parameters out of bounds',
                    'minbound'  : strfdate(minbound),
                    'maxbound'  : strfdate(maxbound),                    
                    'today'     : strfdate(today),
                    'data'      : None,
                }
            return HttpResponse(json.dumps(data), content_type='application/json')
        # Accepted: change the values of lbound and ubound accordingly
        lbound = date
        ubound = date + timedelta(1)
            
    elif lbound and ubound:
        try:
            lbound = strpdate(lbound)
            ubound = strpdate(ubound)
        except ValueError:
            return HttpResponseBadRequest()
            
        if maxbound <= lbound or ubound <= minbound:
            data = {
                    'error'     : 'parameters out of bounds',
                    'minbound'  : strfdate(minbound),
                    'maxbound'  : strfdate(maxbound),                      
                    'today'     : strfdate(today),
                    'data'      : None,
                }
            return HttpResponse(json.dumps(data), content_type='application/json')
        # Accepted: change the values of start_date and end_date accordingly
        lbound = minbound if lbound < minbound else lbound
        ubound = maxbound if maxbound < ubound else ubound
        
    elif lbound or ubound:  
        return HttpResponseBadRequest()
    else:
        # Use defaults
        lbound = minbound
        ubound = maxbound

    data = {
            #'minbound'  : strfdate(minbound),
            #'maxbound'  : strfdate(maxbound),
            'minbound'  : minbound.isoformat(),
            'maxbound'  : maxbound.isoformat(),            
            'today'     : strfdate(today),
            # Change to first available date
            'default'   : strfdate(today),
            'lbound'    : strfdate(lbound),
            'ubound'    : strfdate(ubound),
            'data'      : {strfdate(d): a for d, a in availability(lbound, ubound, location)},
        }

    return HttpResponse(json.dumps(data), content_type='application/json')