from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _

from appointments.apps.timeslots.models import Action, Constraint

# Create your models here.

class Appointment(models.Model):
    
    # Required fields; eventually get rid of this
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appointments')
    
    action = models.ForeignKey(Action, related_name='+',
        verbose_name=_('action'))
    constraint = models.ForeignKey(Constraint, related_name='+',
        verbose_name=_("location"))
    
    date = models.DateField()
    time = models.TimeField()
    
    # Status fields
    status = models.CharField(max_length=2, default='PE', choices=[
            ('PE', 'pending'),
            ('CO', 'confirmed'),
            ('CA', 'cancelled'),            
        ])
        
    def is_pending(self):
        return 'PE' == self.status
        
    @property
    def pending(self):
        return self.is_pending()

    def cancel(self, commit=True):
        self.status = 'CA';
        if commit:
            self.save()

    def is_cancelled(self):
        return 'CA' == self.status
            
    @property
    def cancelled(self):
        return self.is_cancelled()
 
    def confirm(self, commit=True):
        self.status = 'CO';
        if commit:
            self.save()
            
    def is_confirmed(self):
        return 'CO' == self.status
    
    @property
    def confirmed(self):
            return self.is_confirmed()
    

    # Optional fields
    first_name = models.CharField(max_length=64, blank=True, default='',
        verbose_name=_('first name'))
    last_name = models.CharField(max_length=64, blank=True, default='',
        verbose_name=_('last name'))
    nationality = models.CharField(max_length=32, blank=True, default='',
        verbose_name=_('nationality'))
    sex = models.CharField(max_length=1, blank=True, default='',
        choices=(('M', _('Male')), ('F', _('Female')),),
        verbose_name=_('sex'))
        
    identity_number = models.CharField(max_length=64, blank=True, default='',
        verbose_name=_('identity number'))
    document_number = models.CharField(max_length=64, blank=True, default='',
        verbose_name=_('document number'))
    
    phone_number = models.CharField(max_length=16, blank=True, default='',
        verbose_name=_('phone number'))
    mobile_number = models.CharField(max_length=16, blank=True, default='',
        verbose_name=_('mobile number'))

    comment = models.TextField(blank=True, default='',
        verbose_name=_('comment'))    

    # Audit fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def get_url_safe_key(self):
        from .utils import get_serializer
        s = get_serializer()
        return s.dumps(self.pk)
        
    def full_name(self):
        if self.last_name and self.first_name:
            return "%s %s" % (self.first_name, self.last_name)
        if self.last_name and self.sex:
            return "%s %s" % ('Mr.' if 'M' == self.sex else 'Ms.', self.last_name)
        if self.last_name:
            return "Mr./Ms. %s" % (self.last_name)
        if self.first_name:
            return self.first_name
        return ""
        
    class Meta:
        verbose_name = _("appointment")
        verbose_name_plural = _("appointments")
    
    def __unicode__(self):
        return "Appointment id=%s" % (self.pk)


class Report(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_admin': True},
        verbose_name=_('user'))
        
    constraint = models.ForeignKey(Constraint, related_name='+',
        verbose_name=_('location'))

    kind = models.CharField(max_length=2, default='DA', choices = [
            ('DA', 'daily'),
            # ('SP', 'spot'),
        ])
        
    last_sent = models.DateTimeField(null=True, default=None)
    
    enabled = models.BooleanField(default=True)
    
    class Meta:
        unique_together = (('user','constraint',),)
    
    def __unicode__(self):
        return "Report id=%s" % (self.pk)


# Custom user model implementation; uses e-mail for unique id/username
# This implementation is adapted from the Django documentation at
# https://docs.djangoproject.com/en/1.7/topics/auth/customizing/

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.is_active=is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True    
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    first_name = models.CharField(max_length=64, blank=True, default='')
    last_name = models.CharField(max_length=64, blank=True, default='')
    
    constraints = models.ManyToManyField(Constraint, related_name='+', blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)

    def verify(self, commit=True):
        # if self.is_verified:
        #     return
        self.is_verified = True
        if commit:
            self.save()

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return "%s" % (self.email)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin