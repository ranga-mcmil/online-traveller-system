# Generated by Django 5.0.4 on 2024-05-19 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0009_rename_image_accommodation_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accomodationbooking',
            name='adults',
            field=models.IntegerField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='accomodationbooking',
            name='children',
            field=models.IntegerField(blank=True, max_length=255, null=True),
        ),
    ]