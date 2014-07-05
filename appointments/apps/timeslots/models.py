from django.db import models
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

# Create your models here.

class Definition (models.Model):

    json = JSONField(_("Definition"))