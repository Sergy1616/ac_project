from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from .models import Category, Brand, ProductImage, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = (
        'id', 
        'category',
        'name',
        'brand',
        'price',
        'discount',
        'final_price_display',
        'in_stock'
    )
    search_fields = ('name', 'brand',)
    list_display_links = ('name',)
    list_editable = ('price', 'discount', 'in_stock',)
    list_filter = ('category', 'in_stock', 'time_create')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ProductImageInline,)

    def final_price_display(self, obj):
        return obj.final_price()
    final_price_display.short_description = 'Final Price'
