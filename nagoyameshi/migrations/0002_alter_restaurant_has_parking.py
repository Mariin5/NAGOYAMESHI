# Generated by Django 5.0 on 2024-01-23 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nagoyameshi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='has_parking',
            field=models.CharField(max_length=100, verbose_name='駐車場'),
        ),
    ]