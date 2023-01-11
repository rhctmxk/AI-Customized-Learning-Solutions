from django.db import models
from accounts.models import User

# Create your models here.
class Community(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)  # Field name made lowercase.
    user_id = models.ForeignKey(User, db_column='user_Id', on_delete=models.CASCADE)  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=5000, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    filepath = models.FileField(upload_to='community/')
    filetype = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'community'

class Comment(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)  # Field name made lowercase.
    communityid = models.ForeignKey('Community', db_column='communityId', on_delete=models.CASCADE)  # Field name made lowercase.
    user_id = models.ForeignKey(User, db_column='user_Id', on_delete=models.CASCADE)  # Field name made lowercase.
    content = models.CharField(max_length=1000)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'comment'

class Review(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=10, blank=True, null=True)
    job = models.CharField(max_length=10, blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)
    src = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'review'