# Generated by Django 3.2.16 on 2024-09-20 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20240919_2146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('created_at',), 'verbose_name': 'категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('created_at',), 'verbose_name': 'местоположение', 'verbose_name_plural': 'Местоположения'},
        ),
    ]