# Generated by Django 3.2.7 on 2024-01-03 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lvao', '0013_csvdata_data_gouv_json_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvdata',
            old_name='cleaned_adress1',
            new_name='cleaned_address',
        ),
        migrations.RemoveField(
            model_name='csvdata',
            name='cleaned_adress2',
        ),
    ]
