from django.conf import settings
from django.contrib import messages
from django.forms import Form
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _

import dateutil.parser, json

from itsdangerous import BadSignature

from appointments.apps.timeslots.models import Action, Constraint
from appointments.apps.timeslots.utils import strptime

from .forms import ReminderForm
from .models import Appointment, User
from .utils import get_serializer, send_receipt

# Create your views here.

def book(request):
    
    if 'POST' == request.method and request.is_ajax():
        fields = json.loads(request.body)
        
        try:
            user = User.objects.get(email__iexact=fields['email'])
        except KeyError:
            # This is an error; time to log, then fail
            return HttpResponseBadRequest
        except User.DoesNotExist:
            user = User(email=fields['email'], is_active=False)
            user.save()
        
        try:
            action = Action.objects.get(slug=fields['action'])
        except (KeyError, Action.DoesNotExist):
            # This is an error; time to log, then fail
            return HttpResponseBadRequest
        
        try:
            constraint = Constraint.objects.get(slug=fields['constraint'])
        except (KeyError, Constraint.DoesNotExist):
            # This is an error; time to log, then fail
            return HttpResponseBadRequest
            
        if action not in constraint.actions.all():
            # This is an error; time to log, then fail
            return HttpResponseBadRequest

        # Ignore timezone to prevent one-off problems
        try:
            date = dateutil.parser.parse(fields['date'], ignoretz=True).date()
            time = strptime(fields['time'])
        except KeyError:
            # This is an error; time to log, then fail
            return HttpResponseBadRequest        
        
        # Check if timeslot is available
        # Best to preprocess sex
        
        appointment = Appointment(
                user=user,
                action=action,
                constraint=constraint,
                date=date,
                time=time,
                # Optional fields...
                first_name=fields.get('first_name', None),
                last_name=fields.get('last_name', None),
                nationality=fields.get('nationality', None),
                sex=fields['sex'][0].upper() if fields.get('sex', None) else None,
                identity_number=fields.get('identity_number', None),
                document_number=fields.get('document_number', None),
                phone_number=fields.get('phone_number', None),
                mobile_number=fields.get('mobile_number', None),
                comment=fields.get('comment', None),
            )
            
        # Save the appointment
        appointment.save()
        
        send_receipt(request, appointment)
        messages.success(request, _("We've send you an e-mail receipt. Please confirm your appointment by following the instructions."))

        # Return some JSON...
        return HttpResponse("Ok")

    
    elif 'POST' == request.method:
        return HttpResponseBadRequest("XMLHttpRequest (AJAX) form submissions only please!")
    
    return render(request, 'book.html')
    
def cancel(request, payload):
    from itsdangerous import BadSignature
    s = get_serializer()
    try:
        appointment_id = s.loads(payload)
    except BadSignature:
        return Http404
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if appointment.is_cancelled():
        messages.warning(request, _("You've already cancelled this appointment."))    
        return redirect('finish')
    
    if 'POST' == request.method:
        form = Form(request.POST)
        if form.is_valid():    
            appointment.cancel()
            messages.info(request, _("You successfully cancelled your appointment."))
            return redirect('finish')

        # This doesn't seem to be the correct return code
        return Http404
    
    form = Form()
    return render(request, 'cancel.html', {'form': form})

def confirm(request, payload):
    s = get_serializer()
    try:
        appointment_id = s.loads(payload)
    except BadSignature:
        return Http404
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if appointment.is_cancelled():
        messages.error(request, _("You cannot reconfirm a cancelled appointment. Please book again."))
    elif appointment.is_confirmed():
        messages.warning(request, _("Thank you, no need to reconfirm."))        
    else:
        appointment.confirm()
        appointment.user.verify()        
        messages.success(request, _("Thank you for confirming your appointment."))

    return redirect('finish')
    
def reminder(request):
    if 'POST' == request.method:
        form = ReminderForm(request.POST)
        if form.is_valid():
            # Send the reminder
            return redirect('finish')

    else:
        form = ReminderForm()
            
    return render(request, 'reminder.html', {'form': form})