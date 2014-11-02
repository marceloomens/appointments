from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Appointment, Report, User

# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):

    # Override get_form to modify foreignkey behaviour    

    date_hierarchy = 'date'
    fieldsets = (
        (None, {'fields': ('user', 'constraint', 'date', 'time', 'action', 'status')}),
        ('Additional information', {'fields': ('first_name', 'last_name', 'nationality', 'sex',
                'identity_number', 'document_number', 'phone_number', 'mobile_number', 'comment'),
            'classes': ('collapse',)}),
        ('Auditing information', {'fields': ('created', 'modified'),
            'classes': ('collapse',)}),
    )   
    list_display = ('user', 'action', 'constraint', 'date', 'time', 'status')
    list_filter = ('status', 'constraint')
    ordering = ('-date', 'time')
    readonly_fields = ('user', 'date', 'time', 'constraint', 'modified', 'created')
    view_on_site = False
        
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Faster if we query on values?
        if obj and obj.constraint in request.user.constraints.all():
            return True
        if obj:
            return False
        return True
        
    def get_queryset(self, request):
        qs = super(AppointmentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(constraint__in=request.user.constraints.all())
    


class ReportAdmin(admin.ModelAdmin):
    fields = ('user', 'constraint', 'kind', 'last_sent', 'enabled')
    list_display = ('enabled', 'user', 'constraint', 'kind', 'last_sent')
    list_display_links = ('user',)
    readonly_fields = ('last_sent',)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Faster if we query on values?
        if obj and obj.constraint in request.user.constraints.all():
            return True
        if obj:
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
    
    def get_queryset(self, request):
        qs = super(ReportAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(constraint__in=request.user.constraints.all())

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'user':
            # How to logically restrict the set of users?
            # Preferably all users that share at least one contraint with the current user
            pass
        if db_field.name == "constraint":
            kwargs['queryset'] = request.user.constraints.all()
        return super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# Custom user model admdin; uses e-mail for unique id/username
# This implementation is adapted from the Django documentation at
# https://docs.djangoproject.com/en/1.7/topics/auth/customizing/

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        if len(self.cleaned_data["password1"]) < 1:
            # This path is to enable creating new users on the backend
            user.set_unusable_password()
            user.is_active = False
        else:    
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        # Feels hackish
        help_text=("Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('is_active', 'email', 'get_full_name', 'is_admin', 'is_superuser')
    list_display_links = ('email', 'get_full_name')
    list_filter = ('is_active', 'is_admin', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active',)}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser', 'groups', 'constraints' ),
                            'classes': ('collapse',)}),
    )
    filter_horizontal = ('constraints','groups',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Now register the new UserAdmin...
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(User, UserAdmin)