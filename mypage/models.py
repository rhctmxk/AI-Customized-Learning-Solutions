from django.db import models
from accounts.models import User
from search.models import Data_sum_detail1, Technology_korea, Technology_other
#models.DO_NOTHING,

# Create your models here.


class license_select(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)
    license = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Video(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=5000, blank=True, null=True)
    src = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        db_table = 'Video'

class Alert(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)
    content = models.CharField(max_length=5000, blank=True, null=True)
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    activate = models.IntegerField(blank=True, null=True, default=1)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    class Meta:
        db_table = 'Alert'