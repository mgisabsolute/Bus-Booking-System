# Generated by Django 5.1.6 on 2025-02-20 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_trip_tripexpense'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tripexpense',
            name='trip',
        ),
        migrations.DeleteModel(
            name='Trip',
        ),
        migrations.DeleteModel(
            name='TripExpense',
        ),
    ]
