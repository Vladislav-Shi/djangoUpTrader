from django.contrib import admin

from app import models


class BaseMenuAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "parent", "level"]
    readonly_fields = ["level"]


admin.site.register(models.BaseMenu, BaseMenuAdmin)
admin.site.register(models.CategoryMenu)
