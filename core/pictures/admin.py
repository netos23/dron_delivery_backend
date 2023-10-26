from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import PictureModel


# admin.site.register(PictureModel)


@admin.register(PictureModel)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', "picture_image",   "created_at", "expiration_date")

    def picture_image(self, obj):
        return mark_safe(f'<img src="{obj.link or ""}" width="150" height="150" /> ')
