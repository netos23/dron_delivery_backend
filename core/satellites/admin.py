from django.contrib import admin
from django.utils.safestring import mark_safe

from satellites.models import SatelliteModel

# Register your models here.
@admin.register(SatelliteModel)
class SatelliteModel(admin.ModelAdmin):
    list_display = ('object_id', "picture_image", "object_name", "is_active")

    def picture_image(self, obj):
        return mark_safe(f'<img src="{obj.picture or ""}" width="150" height="150" /> ')