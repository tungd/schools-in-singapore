from django.contrib import admin

from . import models


@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    list_per_page = 20
