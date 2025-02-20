# Generated by Django 5.1.6 on 2025-02-19 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_bus_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={},
        ),
        migrations.RemoveField(
            model_name='bus',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='bus',
            name='is_active',
        ),
        migrations.AddField(
            model_name='book',
            name='seat_class',
            field=models.CharField(choices=[('GEN', 'General'), ('SLP', 'Sleeper'), ('LUX', 'Luxury')], default='GEN', max_length=3),
        ),
        migrations.AddField(
            model_name='bus',
            name='seat_class',
            field=models.CharField(choices=[('GEN', 'General'), ('SLP', 'Sleeper'), ('LUX', 'Luxury')], default='GEN', max_length=3),
        ),
        migrations.DeleteModel(
            name='BusSchedule',
        ),
    ]
