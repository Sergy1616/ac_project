# Generated by Django 4.2.7 on 2024-05-30 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, default='Wish List', max_length=255)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('products', models.ManyToManyField(blank=True, related_name='in_wishlist', to='shop.product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
    ]
