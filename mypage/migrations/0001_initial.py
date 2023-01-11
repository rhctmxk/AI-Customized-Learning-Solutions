# Generated by Django 4.1 on 2022-10-07 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('pk_id', models.AutoField(db_column='PK_ID', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('url', models.CharField(blank=True, max_length=5000, null=True)),
                ('src', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'Video',
            },
        ),
        migrations.CreateModel(
            name='license_select',
            fields=[
                ('pk_id', models.AutoField(db_column='PK_ID', primary_key=True, serialize=False)),
                ('license', models.CharField(blank=True, max_length=50, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('pk_id', models.AutoField(db_column='PK_ID', primary_key=True, serialize=False)),
                ('content', models.CharField(blank=True, max_length=5000, null=True)),
                ('activate', models.IntegerField(blank=True, default=1, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Alert',
            },
        ),
    ]