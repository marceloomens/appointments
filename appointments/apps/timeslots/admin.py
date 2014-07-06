from django.contrib import admin

from jsonfield import JSONCharField
from django.forms import Textarea

from .models import ConstraintSet, Constraint, Definition, Holiday

# Register your models here.

class ConstraintAdmin(admin.TabularInline):

    extra = 0
    fields = ('name', 'slug', 'enabled',)
    model = Constraint
    prepopulated_fields = {'slug': ('name',)}


class ConstraintSetAdmin(admin.ModelAdmin):

    inlines = (ConstraintAdmin,)
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
    
    
admin.site.register(ConstraintSet, ConstraintSetAdmin)
admin.site.register(Definition, DefinitionAdmin)
admin.site.register(Holiday, HolidayAdmin)