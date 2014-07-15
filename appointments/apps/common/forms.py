from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Appointment


class AppointmentForm(forms.ModelForm):

    class Meta:
        # exclude = []
        model = Appointment
        
    
class ReminderForm(forms.Form):

    email = forms.EmailField(label=_("e-mail address"), required=True)