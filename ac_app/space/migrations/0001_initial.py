# Generated by Django 4.2.7 on 2024-05-26 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='space_news/%Y/%m/%d/')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'news',
                'verbose_name_plural': 'space news',
                'ordering': ['-time_create'],
            },
        ),
    ]
