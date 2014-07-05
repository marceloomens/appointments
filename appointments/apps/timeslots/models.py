from django.db import models
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

# Create your models here.

#  TO DO
# - Generalize constraints
# - Allow multiple constraints per Definition

class ConstraintSet (models.Model):

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural =  _("Locations")
    
    def __str__(self):
        return  "<ConstraintSet/Location: %s>" % (self.name)
        
    # def choices(self):
    #     return [(value.slug, value.name) for value in self.values.all() if value.enabled]
            
            
class Constraint (models.Model):

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)

    key = models.ForeignKey(ConstraintSet, related_name='values')

    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural =  _("Cities")
        
    def __str__(self):
        return "<Constraint/Location: %s, %s>" % (self.key.name, self.name)


class Definition (models.Model):

    constraint = models.ForeignKey(Constraint)
    
    json = JSONField(_("Definition"))
    
    class Meta:
        verbose_name = _("Timeslots")
        verbose_name_plural = _("Timeslots")
        
    def __str__(self):
        return "<Definition id=%s>" % (self.pk)