import cms.models

from django.contrib import admin
from deuse_formation.admin import admin_site


@admin.register(cms.models.CustomHTMLContent, site=admin_site)
class CustomHTMLContentAdmin(admin.ModelAdmin):
    list_display = ('token',)
    search_fields = ('token',)
    readonly_fields = ('token',)
    fields = ('token', 'content')
