# Generated by Django 4.1 on 2022-10-10 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='technology_korea',
            old_name='qual',
            new_name='license',
        ),
        migrations.RenameField(
            model_name='technology_other',
            old_name='qual',
            new_name='license',
        ),
    ]
