# Generated by Django 3.2.7 on 2024-01-03 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lvao', '0006_auto_20240103_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvfileprocess',
            name='progress',
            field=models.FloatField(default=0),
        ),
    ]
