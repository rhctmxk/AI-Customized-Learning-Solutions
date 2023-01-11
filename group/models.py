from django.db import models
from accounts.models import User
from main.models import Community

# Create your models here.

class GroupStudy(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=5000, blank=True, null=True)
    recruitment_start_date = models.DateTimeField(blank=True, null=True)
    recruitment_end_date = models.DateTimeField(blank=True, null=True)
    activity_start_date = models.DateTimeField(blank=True, null=True)
    activity_end_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'groupStudy'

class GroupStudyComment(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)  # Field name made lowercase.
    groupstudyid = models.ForeignKey(GroupStudy, models.DO_NOTHING, db_column='groupstudyid')  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    content = models.CharField(max_length=1000)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'groupstudycomment'



class GroupInfo(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)  # Field name made lowercase.
    groupstudyid = models.ForeignKey(GroupStudy, models.DO_NOTHING, db_column='groupstudyid')  # Field name made lowercase.
    mentorid = models.ForeignKey(User, models.DO_NOTHING, db_column='mentorId')  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=5000, blank=True, null=True)
    recruitment_start_date = models.DateTimeField(blank=True, null=True)
    recruitment_end_date = models.DateTimeField(blank=True, null=True)
    activity_start_date = models.DateTimeField(blank=True, null=True)
    activity_end_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    filepath = models.FileField(upload_to='group/')
    filetype = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'group_info'

class GroupBoard(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    groupinfoid = models.ForeignKey(GroupInfo, models.DO_NOTHING, db_column='groupinfoId')  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=5000, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    filepath = models.FileField(upload_to='groupboard/')
    filetype = models.CharField(max_length=100, blank=True, null=True)
    is_notice = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'group_board'


class GroupComment(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)  # Field name made lowercase.
    groupboardid = models.ForeignKey(GroupBoard, models.DO_NOTHING, db_column='groupboardId')  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    content = models.CharField(max_length=1000)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'group_comment'



class GroupUser(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid')
    groupinfoid = models.ForeignKey(GroupInfo, models.DO_NOTHING, db_column='groupinfoId')  # Field name made lowercase.
    is_waiting = models.IntegerField(blank=True, null=True)
    is_registered = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'group_user'

