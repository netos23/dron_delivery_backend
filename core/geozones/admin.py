from django.contrib import admin
from geozones.models import GeozoneModel, DeprecatedGeozoneModel



@admin.register(GeozoneModel)
class GeozoneAdmin(admin.ModelAdmin):
    list_display = ('id', "name", "wkt")

@admin.register(DeprecatedGeozoneModel)
class DeprecatedGeozoneModelAdmin(admin.ModelAdmin):
    list_display = ('id', "name", "wkt")
