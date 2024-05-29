from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products_by_category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']


class Brand(models.Model):
    def upload_img(self, filename):
        return f'brands/{self.slug}/{filename}'

    name = models.CharField(max_length=100, db_index=True, unique=True, verbose_name='Brand')
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    image = models.ImageField(upload_to=upload_img, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products_by_brand', kwargs={'brand_slug': self.slug})

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, models.SET_NULL, blank=True, null=True, default=None)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Discount %',
        help_text='Percentage value (0 to 100)'
    )
    time_create = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-time_create', 'name']

    def final_price(self):
        if self.discount:
            discount_amount = (self.price * self.discount) / 100
            return round(self.price - discount_amount, 2)
        return self.price


class ProductImage(models.Model):
    def upload_img(self, filename):
        return f'product_images/{self.product.category.slug}/{self.product.slug}/{filename}'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_img, blank=True)
    title_image = models.BooleanField(default=False)
    is_for_slider = models.BooleanField(default=False)
