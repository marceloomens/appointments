from django.contrib import admin

from jsonfield import JSONCharField
from django.forms import Textarea

from .models import ConstraintSet, Constraint, Definition

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
    # list_display = ('start_date', 'constraint', 'kind', 'encoding')
    # readonly_fields = ('end_date', 'enabled')
    fields = ('constraint','valid', 'until', 'json', 'enabled',)
    list_display = ('constraint', 'valid', 'until', 'enabled',)
    readonly_fields = ('until',)
    
    
admin.site.register(ConstraintSet, ConstraintSetAdmin)
admin.site.register(Definition, DefinitionAdmin)