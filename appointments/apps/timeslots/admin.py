from django.contrib import admin

from jsonfield import JSONCharField
from django.forms import Textarea

from .models import Action, ConstraintSet, Constraint, Definition, Holiday

# Register your models here.

class ActionAdmin(admin.ModelAdmin):

    fields = ('name', 'slug', 'enabled',)
    list_display = ('name', 'slug', 'enabled',)
    prepopulated_fields = {'slug': ('name',)}
    view_on_site = False

    def get_actions(self, request):
        actions = super(ActionAdmin, self).get_actions(request)
        if not self.has_delete_permission(request):
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


class ConstraintAdmin(admin.ModelAdmin):
    
    fields = ('name', 'slug', 'enabled', 'timezone', 'actions',)
    filter_horizontal = ('actions',)
    list_display = ('name', 'timezone', 'slug', 'enabled',)
    readonly_fields = ('name', 'slug',)
    view_on_site = False
    
    def get_actions(self, request):
        actions = super(ConstraintAdmin, self).get_actions(request)
        if not self.has_delete_permission(request):
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ConstraintAdmin, self).get_queryset(request)
        return request.user.constraints.all()
        
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj in request.user.constraints.all():
            return True
        if obj:
            return False
        return True


class ConstraintInlineAdmin(admin.TabularInline):

    extra = 0
    fields = ('name', 'slug', 'enabled',)
    model = Constraint
    prepopulated_fields = {'slug': ('name',)}
    view_on_site = False


class ConstraintSetAdmin(admin.ModelAdmin):

    inlines = (ConstraintInlineAdmin,)
    fields = ('name', 'slug', 'enabled',)
    list_display = ('name', 'slug', 'enabled',)
    prepopulated_fields = {'slug': ('name',)}
    view_on_site = False
    

class DefinitionAdmin(admin.ModelAdmin):

    fields = ('constraint','valid', 'until', 'json', 'enabled',)
    list_display = ('constraint', 'valid', 'until', 'enabled',)
    readonly_fields = ('until',)
    view_on_site = False
    
    
class HolidayAdmin(admin.ModelAdmin):

    fields = ('constraint', 'date', 'reason', 'enabled',)
    list_display = ('constraint', 'date', 'reason', 'enabled',)
    view_on_site = False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(HolidayAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'constraint':
            kwargs['queryset'] = request.user.constraints.all()
        return super(HolidayAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(HolidayAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(constraint__in=request.user.constraints.all())

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.constraint in request.user.constraints.all():
            return True
        if obj:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
    

admin.site.register(Action, ActionAdmin)
admin.site.register(Constraint, ConstraintAdmin)
admin.site.register(ConstraintSet, ConstraintSetAdmin)
admin.site.register(Definition, DefinitionAdmin)
admin.site.register(Holiday, HolidayAdmin)
