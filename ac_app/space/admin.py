from django.contrib import admin

from .models import SpaceNews, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['news']
    extra = 1


@admin.register(SpaceNews)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'image', 'published')
    list_display_links = ('title',)
    search_fields = ('time_create',)
    list_editable = ('published',)
    list_filter = ('published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]
