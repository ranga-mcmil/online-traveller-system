# Generated by Django 5.0.4 on 2024-05-19 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0011_accomodationbooking_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accomodationbooking',
            name='adults',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='accomodationbooking',
            name='children',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]