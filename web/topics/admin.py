from django.contrib import admin
from deuse_formation.admin import admin_site

from .models import Topic, Response, SlugHistory

# admin_site.register(Topics)

@admin.register(Topic, site=admin_site)
class TopicAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        (
            None,
            {
                'fields': ['name', 'description', 'user', 'slug']
            }
        ),
        (
            'Dates importantes',
            {
                'fields': ['created_at', 'updated_at']
            }
        )
    ]
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name', ]
    list_filter = ['user', 'created_at']

admin_site.register(Response)
admin_site.register(SlugHistory)