# Generated by Django 5.0.4 on 2024-05-19 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0010_alter_accomodationbooking_adults_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accomodationbooking',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]