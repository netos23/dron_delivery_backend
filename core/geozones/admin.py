from django.contrib import admin
from geozones.models import GeozoneModel, DeprecatedGeozoneModel

admin.site.register(DeprecatedGeozoneModel)


@admin.register(GeozoneModel)
class GeozoneAdmin(admin.ModelAdmin):
    list_display = ('id', "name", "wkt")
