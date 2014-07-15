from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Appointment

# Create your views here.

def book(request):
    # I would much prefer to set ng_app in my template
    return render(request, 'book.html', {'ng_app': True})
    
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