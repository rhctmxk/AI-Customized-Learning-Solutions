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
            name='GroupBoard',
            fields=[
                ('pk_id', models.AutoField(db_column='PK_ID', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.CharField(blank=True, max_length=5000, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('filepath', models.FileField(upload_to='groupboard/')),
                ('filetype', models.CharField(blank=True, max_length=100, null=True)),
                ('is_notice', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'group_board',
            },
        ),
        migrations.CreateModel(
            name='GroupInfo',
            fields=[
                ('pk_id', models.AutoField(db_column='PK_ID', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.CharField(blank=True, max_length=5000, null=True)),
                ('recruitment_start_date', models.DateTimeField(blank=True, null=True)),
                ('recruitment_end_date', models.DateTimeField(blank=True, null=True)),
                ('activity_start_date', models.DateTimeField(blank=True, null=True)),
                ('activity_end_date', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('filepath', models.FileField(upload_to='group/')),
                ('filetype', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'group_info',
            },
        ),
        migrations.CreateModel(
            name='GroupStudy',
            fields=[
                ('pk_id', models.AutoField(db_column='PK_ID', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.CharField(blank=True, max_length=5000, null=True)),
                ('recruitment_start_date', models.DateTimeField(blank=True, null=True)),
                ('recruitment_end_date', models.DateTimeField(blank=True, null=True)),
                ('activity_start_date', models.DateTimeField(blank=True, null=True)),
                ('activity_end_date', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('userid', models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'groupStudy',
            },
        ),
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('pk_id', models.AutoField(db_column='PK_ID', primary_key=True, serialize=False)),
                ('is_waiting', models.IntegerField(blank=True, null=True)),
                ('is_registered', models.IntegerField(blank=True, null=True)),
                ('groupinfoid', models.ForeignKey(db_column='groupinfoId', on_delete=django.db.models.deletion.DO_NOTHING, to='group.groupinfo')),
                ('userid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'group_user',
            },
        ),
        migrations.CreateModel(
            name='GroupStudyComment',
            fields=[
                ('pk_id', models.AutoField(db_column='PK_ID', primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=1000)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('groupstudyid', models.ForeignKey(db_column='groupstudyid', on_delete=django.db.models.deletion.DO_NOTHING, to='group.groupstudy')),
                ('userid', models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'groupstudycomment',
            },
        ),
        migrations.AddField(
            model_name='groupinfo',
            name='groupstudyid',
            field=models.ForeignKey(db_column='groupstudyid', on_delete=django.db.models.deletion.DO_NOTHING, to='group.groupstudy'),
        ),
        migrations.AddField(
            model_name='groupinfo',
            name='mentorid',
            field=models.ForeignKey(db_column='mentorId', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='GroupComment',
            fields=[
                ('pk_id', models.AutoField(db_column='PK_ID', primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=1000)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('groupboardid', models.ForeignKey(db_column='groupboardId', on_delete=django.db.models.deletion.DO_NOTHING, to='group.groupboard')),
                ('userid', models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'group_comment',
            },
        ),
        migrations.AddField(
            model_name='groupboard',
            name='groupinfoid',
            field=models.ForeignKey(db_column='groupinfoId', on_delete=django.db.models.deletion.DO_NOTHING, to='group.groupinfo'),
        ),
        migrations.AddField(
            model_name='groupboard',
            name='userid',
            field=models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]