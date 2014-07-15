from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _

from appointments.apps.timeslots.models import Action, Constraint

# Create your models here.

class Appointment(models.Model):
    
    # Required fields
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
        
    def cancel(self, commit=True):
        self.status = 'CA';
        if commit:
            self.save()
 
    def confirm(self, commit=True):
        self.status = 'CO';
        if commit:
            self.save()

    # Optional fields
    first_name = models.CharField(max_length=64, blank=True,
        verbose_name=_('first name'))
    last_name = models.CharField(max_length=64, blank=True,
        verbose_name=_('last name'))
    nationality = models.CharField(max_length=32, blank=True,
        verbose_name=_('nationality'))
    sex = models.CharField(max_length=1, blank=True,
        choices=(('M', _('Male')), ('F', _('Female')),),
        verbose_name=_('sex'))
        
    identity_number = models.CharField(max_length=64, blank=True,
        verbose_name=_('identity number'))
    document_number = models.CharField(max_length=64, blank=True,
        verbose_name=_('document number'))
    
    phone_number = models.CharField(max_length=16, blank=True,
        verbose_name=_('phone number'))
    mobile_number = models.CharField(max_length=16, blank=True,
        verbose_name=_('mobile number'))

    comment = models.TextField(blank=True,
        verbose_name=_('comment'))    

    # Audit fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    # Utility methods
    def get_absolute_url(self):
        # Return admin URL or confirmation url?
        pass

    def get_url_safe_key(self):
        from .utils import get_serializer
        s = get_serializer()
        return s.dumps(self.pk)
        
    class Meta:
        verbose_name = _("appointment")
        verbose_name_plural = _("appointments")
    
    def __unicode__(self):
        return "<Appointment object: user=%s>" % (self.user.get_short_name())


class Report(models.Model):
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_admin': True},
        verbose_name=_('user'))
        
    constraint = models.ForeignKey(Constraint, related_name='+',
        verbose_name=_('location'))

    kind = models.CharField(max_length=2, default='DA', choices = [
            ('DA', 'daily'),
            # ('SP', 'spot'),
        ])
    
    enabled = models.BooleanField(default=True)


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
        user.is_active=True
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
    
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)

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
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return "<User object: %s>" % (self.email)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
        
        
# Register my signal listener
from .utils import availability_for_range_handler