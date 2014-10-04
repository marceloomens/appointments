from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Appointment

    
class ReminderForm(forms.Form):

    # Validate e-mail; check that this user exists

    email = forms.EmailField(label=_("e-mail address"), required=True)