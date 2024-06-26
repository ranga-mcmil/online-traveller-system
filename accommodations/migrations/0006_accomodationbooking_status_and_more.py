# Generated by Django 5.0.4 on 2024-05-01 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0005_alter_accomodationbooking_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accomodationbooking',
            name='status',
            field=models.CharField(choices=[('BOOKED', 'BOOKED'), ('PENDING', 'PENDING'), ('CANCELLED', 'CANCELLED')], default='PENDING', max_length=50),
        ),
        migrations.AddField(
            model_name='accomodationbooking',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
