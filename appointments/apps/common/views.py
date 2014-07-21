from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

import dateutil.parser, json

from appointments.apps.timeslots.models import Action, Constraint
from appointments.apps.timeslots.utils import strptime

from .forms import ReminderForm
from .models import Appointment, User

# Create your views here.

def book(request):
    
    if 'POST' == request.method and request.is_ajax():
        fields = json.loads(request.body)
        
        try:
            user = User.objects.get(email=fields['email'])
        except User.DoesNotExist:
            user = User(email=fields['email'], is_active=False)
        
        try:
            action = Action.objects.get(slug=fields['action'])
        except Action.DoesNotExist:
            # This is an error; time to fail
            pass
        
        try:
            constraint = Constraint.objects.get(slug=fields['constraint'])
        except Constraint.DoesNotExist:
            # This is an error; time to fail
            pass
            
        if action not in constraint.actions.all():
            # This is an error; time to fail
            pass            

        date = dateutil.parser.parse(fields['date']).date()
        time = strptime(fields['time'])
        
        appointment = Appointment(
                user=user,
                action=action,
                constraint=constraint,
                date=date,
                time=time
            )
            
        # Save the appointment
        print("Yay!")
        print(appointment)

    
    elif 'POST' == request.method:
        pass
    
    return render(request, 'book.html')
    
def cancel(request, payload):
    return render(request, 'cancel.html')

def confirm(request, payload):
    from itsdangerous import BadSignature
    from .utils import get_serializer

    s = get_serializer()
    try:
        appointment_id = s.loads(payload)
    except BadSignature:
        return Http404
    
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    appointment.confirm()
    appointment.user.verify()
    
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