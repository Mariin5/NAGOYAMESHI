# Generated by Django 5.0 on 2024-03-13 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nagoyameshi', '0006_review_star'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.CharField(max_length=100, verbose_name='内容'),
        ),
    ]