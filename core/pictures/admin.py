from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import PictureModel
# admin.site.register(PictureModel)


@admin.register(PictureModel)
class PictureAdmin(admin.ModelAdmin):
    list_display = ("picture_image",'id', 'url', "link")

    def picture_image(self, obj):
        return mark_safe(f'<img src="{obj.link or obj.url or ""}" width="150" height="150" /> ')
