from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AppointmentForm, ReminderForm
from .models import Appointment

# Create your views here.

def book(request):
    # I would much prefer to set ng_app in my template
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