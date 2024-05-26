from django.contrib import admin

from .models import SpaceNews


@admin.register(SpaceNews)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'image', 'published')
    list_display_links = ('title',)
    search_fields = ('time_create',)
    list_editable = ('published',)
    list_filter = ('published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
