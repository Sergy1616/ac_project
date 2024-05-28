# Generated by Django 4.2.7 on 2024-05-28 14:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import space.models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0003_constellation'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpectralClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('image', models.FileField(blank=True, upload_to='Spectrum_svg/', validators=[django.core.validators.FileExtensionValidator(['png', 'svg'])])),
                ('color', models.CharField(max_length=50)),
                ('temperature', models.CharField(max_length=50)),
                ('features', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Spectral classes',
                'ordering': ['id', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to=space.models.Star.upload_img)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('constellation', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='space.constellation')),
                ('spectrum', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='space.spectralclass')),
            ],
            options={
                'ordering': ['name', 'spectrum'],
            },
        ),
    ]
