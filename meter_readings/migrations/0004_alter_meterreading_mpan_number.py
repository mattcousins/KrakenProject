# Generated by Django 4.1.7 on 2023-02-19 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meter_readings', '0003_meterreading_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meterreading',
            name='mpan_number',
            field=models.BigIntegerField(),
        ),
    ]
