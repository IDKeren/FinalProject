# Generated by Django 5.1 on 2024-09-12 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_logs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logs',
            old_name='drone_id',
            new_name='drone',
        ),
    ]