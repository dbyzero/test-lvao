# Generated by Django 3.2.7 on 2024-01-03 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lvao', '0005_remove_csvdata_csvfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvdata',
            name='cleaned_address_for_hash',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='csvdata',
            name='cleaned_gps_for_hash',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
