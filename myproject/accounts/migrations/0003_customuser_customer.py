# Generated by Django 5.0 on 2024-02-07 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_delete_gender_customuser_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='customer',
            field=models.TextField(blank=True, null=True, verbose_name='有料会員'),
        ),
    ]