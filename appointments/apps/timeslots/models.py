from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

import pytz

# Create your models here.

class Action (models.Model):

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
        
    enabled = models.BooleanField(default=True) 

    class Meta:
        verbose_name = _("action")
        verbose_name_plural =  _("actions")
    
    def __unicode__(self):
        return  "%s" % (self.name)


class ConstraintSet (models.Model):

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("country")
        verbose_name_plural =  _("countries")
    
    def __unicode__(self):
        return  "%s" % (self.name)
            
            
class Constraint (models.Model):

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)

    key = models.ForeignKey(ConstraintSet, related_name='values')
    actions = models.ManyToManyField(Action, related_name='constraints', blank=True)
    
    timezone = models.CharField(max_length=32, default=settings.TIME_ZONE,
        choices=list((x,x) for x in pytz.common_timezones))

    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("city")
        verbose_name_plural =  _("cities")
        
    def __unicode__(self):
        return "%s, %s" % (self.name, self.key.name)


class Definition (models.Model):

    constraint = models.ForeignKey(Constraint, verbose_name=_("location"), related_name='definitions')
    
    json = JSONField(_("definition"))
    
    valid = models.DateField(_("from"))
    # I run into all sorts of problems when definitions don't extend until TIMESLOTS_FUTURE
    until = models.DateField(_("until"), blank=True, null=True, default=None, editable=False)    
    
    enabled = models.BooleanField(default=True)
    
    @cached_property
    def timeslots(self):
        from .utils import WEEKDAYS, strptime
        defaults = self.json.get('defaults', None)
        return {
                weekday: { strptime(t): a for (t, a) in self.json.get(weekday, defaults).items() }
                    if self.json.get(weekday, defaults)
                    else []
                for weekday in WEEKDAYS
            }
    
    class Meta:
        ordering = ['-valid']
        verbose_name = _("timeslots")
        verbose_name_plural = _("timeslots")
        
    def __unicode__(self):
        return "Definition id=%s" % (self.pk)
        
        
class Holiday (models.Model):
    
    constraint = models.ForeignKey(Constraint, verbose_name=_("location"), related_name='holidays')    

    date = models.DateField(_("date"))
    reason = models.CharField(_("reason"), max_length=128)

    enabled = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("holiday")
        verbose_name_plural =  _("holiday")
        
    def __unicode__(self):
        return "Holiday id=%s" % (self.pk)    