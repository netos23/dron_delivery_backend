from django.contrib import admin

from geozones.models import GeozoneModel

# Register your models here.

# admin.site.register(GeozoneModel)

@admin.register(GeozoneModel)
class GeozoneAdmin(admin.ModelAdmin):
    list_display = ('id', "name",   "wkt")
