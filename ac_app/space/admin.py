from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import (
    SpaceNews,
    Comment,
    Constellation,
    SpectralClass,
    Star,
    StarCharacteristics,
    FavoriteStar
)


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


class ConstellationAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Constellation
        fields = '__all__'


@admin.register(Constellation)
class ConstellationAdmin(admin.ModelAdmin):
    form = ConstellationAdminForm
    list_display = ('name', 'quadrant', 'time_create', 'image')
    search_fields = ('name', 'quadrant', 'time_create')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SpectralClass)
class SpectralClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


class StarAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Star
        fields = '__all__'


class StarCharacteristicsInline(admin.StackedInline):
    model = StarCharacteristics
    extra = 0


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    form = StarAdminForm
    list_display = ('name', 'id', 'spectrum', 'time_create', 'image')
    search_fields = ('name', 'description')
    list_filter = ('spectrum', )
    prepopulated_fields = {'slug': ('name',)}
    inlines = (StarCharacteristicsInline,)


@admin.register(FavoriteStar)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'star', 'date_added']
    list_filter = ['date_added']
    search_fields = ['user__username', 'star__name']
