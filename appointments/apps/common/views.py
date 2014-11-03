from django.conf import settings
from django.contrib import messages
from django.forms import Form
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.translation import ugettext as _

import dateutil.parser, json

from itsdangerous import BadSignature

from appointments.apps.timeslots.models import Action, Constraint
from appointments.apps.timeslots.utils import strfdate, strftime, strptime, is_available

from .forms import ReminderForm
from .models import Appointment, User
from .utils import get_logger, get_serializer, send_confirmation, send_receipt, send_reminder

# Create your views here.

def book(request):

    logger = get_logger(__name__, request)
    
    if 'POST' == request.method and request.is_ajax():
        fields = json.loads(request.body)
        
        try:
            user = User.objects.get(email__iexact=fields['email'])
        except KeyError:
            # This is an error; time to log, then fail
            logger.warning("Bad form submission: KeyError (email)")
            return HttpResponseBadRequest()
        except User.DoesNotExist:
            user = User(email=fields['email'], is_active=False)
            user.save()
            logger.info("New user %s" % (str(user)))

        try:
            action = Action.objects.get(slug=fields['action'])
        except (KeyError, Action.DoesNotExist):
            logger.warning("Bad form submission: KeyError (action) or Action.DoesNotExist")
            # This is an error; time to log, then fail
            return HttpResponseBadRequest()
        
        try:
            constraint = Constraint.objects.get(slug=fields['constraint'])
        except (KeyError, Constraint.DoesNotExist):
            # This is an error; time to log, then fail
            logger.warning("Bad form submission: KeyError (constraint) or Constraint.DoesNotExist")
            return HttpResponseBadRequest()
            
        if action not in constraint.actions.all():
            # This is an error; time to log, then fail
            logger.warning("Bad form submission: bad constraint/action combination")
            return HttpResponseBadRequest()

        # Ignore timezone to prevent one-off problems
        try:
            date = dateutil.parser.parse(fields['date'], ignoretz=True).date()
            time = strptime(fields['time'])
        except KeyError:
            # This is an error; time to log, then fail
            logger.warning("Bad form submission: KeyError (date and/or time)")
            return HttpResponseBadRequest()
        
        # Check if timeslot is available
        if not is_available(constraint, date, time):
            # Return some meaningful JSON to say that time is not available
            logger.warning("Bad form submission: timeslot not available")
            return HttpResponseBadRequest()            
        
        # Preprocess sex to ensure it's a valid value
        sex = fields['sex'][0].upper() if fields.get('sex', None) else None
        if sex not in ['M', 'F']:
            sex = ''
        
        appointment = Appointment(
                user=user,
                action=action,
                constraint=constraint,
                date=date,
                time=time,
                # Optional fields...
                first_name=fields.get('first_name',''),
                last_name=fields.get('last_name',''),
                nationality = fields.get('nationality',''),
                sex=sex,
                # See if this works without any changes...
                identity_number=fields.get('identity_number',''),
                document_number=fields.get('document_number',''),
                phone_number=fields.get('phone_number',''),
                mobile_number=fields.get('mobile_number',''),
                comment=fields.get('comment',''),
            )
            
        # Save the appointment; then log it
        appointment.save()
        logger.info("New appointment by %s in %s/%s on %s at %s" % (
                    str(appointment.user),
                    appointment.constraint.key.slug,
                    appointment.constraint.slug,
                    strfdate(appointment.date),
                    strftime(appointment.time),
                )
            )
            
        send_receipt(appointment)
        messages.success(request, _("We've send you an e-mail receipt. Please confirm your appointment by following the instructions."))

        # Return some JSON...
        return HttpResponse("Ok")

    
    elif 'POST' == request.method:
        logger.warning("XMLHttpRequest header not set on POST request")
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
        send_confirmation(appointment)    
        messages.success(request, _("Thank you for confirming your appointment."))

    return redirect('finish')
    
def reminder(request):
    if 'POST' == request.method:
        form = ReminderForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                date = timezone.now().date()
                appointments = user.appointments.filter(date__gte=date)
                send_reminder(user, appointments)
                
            except User.DoesNotExist:
                pass

            messages.success(request, _("We'll send you an e-mail with all your appointments."))
            return redirect('finish')

    else:
        form = ReminderForm()
            
    return render(request, 'reminder.html', {'form': form})
    
# Custom error views
    
def handler404(request):
    return render(request, '404.html')