# Generated by Django 3.2.7 on 2024-01-03 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lvao', '0004_auto_20240103_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csvdata',
            name='csvfile',
        ),
    ]
