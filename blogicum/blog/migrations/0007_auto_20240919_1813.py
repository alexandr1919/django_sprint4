# Generated by Django 3.2.16 on 2024-09-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20240919_0705'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('created_at',), 'verbose_name': 'местоположение', 'verbose_name_plural': 'Местоположения'},
        ),
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
