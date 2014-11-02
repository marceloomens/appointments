from django.contrib import admin

from jsonfield import JSONCharField
from django.forms import Textarea

from .models import Action, ConstraintSet, Constraint, Definition, Holiday

# Register your models here.

class ActionAdmin(admin.ModelAdmin):

    fields = ('name', 'slug', 'enabled',)
    list_display = ('name', 'slug', 'enabled',)
    prepopulated_fields = {'slug': ('name',)}


class ConstraintAdmin(admin.ModelAdmin):
    
    fields = ('name', 'slug', 'enabled', 'timezone', 'actions',)
    filter_horizontal = ('actions',)
    list_display = ('name', 'timezone', 'slug', 'enabled',)
    readonly_fields = ('name', 'slug',)
    
    def has_add_permission(self, request):
        return False


class ConstraintInlineAdmin(admin.TabularInline):

    extra = 0
    fields = ('name', 'slug', 'enabled',)
    model = Constraint
    prepopulated_fields = {'slug': ('name',)}


class ConstraintSetAdmin(admin.ModelAdmin):

    inlines = (ConstraintInlineAdmin,)
    fields = ('name', 'slug', 'enabled',)
    list_display = ('name', 'slug', 'enabled',)
    prepopulated_fields = {'slug': ('name',)}
    

class DefinitionAdmin(admin.ModelAdmin):

    fields = ('constraint','valid', 'until', 'json', 'enabled',)
    list_display = ('constraint', 'valid', 'until', 'enabled',)
    readonly_fields = ('until',)
    
    
class HolidayAdmin(admin.ModelAdmin):
    fields = ('constraint', 'date', 'reason', 'enabled')
    list_display = ('constraint', 'date', 'reason', 'enabled')    
    

admin.site.register(Action, ActionAdmin)
admin.site.register(Constraint, ConstraintAdmin)
admin.site.register(ConstraintSet, ConstraintSetAdmin)
admin.site.register(Definition, DefinitionAdmin)
admin.site.register(Holiday, HolidayAdmin)