from django.db import models
from accounts.models import User

# Create your models here.
class Note(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    note = models.CharField(max_length=100, blank=True, null=True)
    page = models.IntegerField(default=1, blank=True, null=True)
    subject = models.IntegerField(blank=True, null=True)
    dib = models.IntegerField(default=0, blank=True, null=True)

class Page(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    page_subject1 = models.IntegerField(default=1, blank=True, null=True)
    page_subject2 = models.IntegerField(default=1, blank=True, null=True)
    page_subject3 = models.IntegerField(default=1, blank=True, null=True)
    page_subject4 = models.IntegerField(default=1, blank=True, null=True)
    page_subject5 = models.IntegerField(default=1, blank=True, null=True)
    dib_subject1 = models.IntegerField(default=0, blank=True, null=True)
    dib_subject2 = models.IntegerField(default=0, blank=True, null=True)
    dib_subject3 = models.IntegerField(default=0, blank=True, null=True)
    dib_subject4 = models.IntegerField(default=0, blank=True, null=True)
    dib_subject5 = models.IntegerField(default=0, blank=True, null=True)