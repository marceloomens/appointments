from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Appointment

# Create your views here.

def book(request):
    return render(request, 'common.html')
    
def cancel(request, payload):
    pass

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
    
    return render(request, 'confirm.html')
    
def remind(request):
    pass