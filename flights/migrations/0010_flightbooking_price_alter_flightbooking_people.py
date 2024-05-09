# Generated by Django 5.0.4 on 2024-05-09 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0009_generatedroute_price_flightbooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightbooking',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='flightbooking',
            name='people',
            field=models.IntegerField(default=1),
        ),
    ]
