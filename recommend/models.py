from django.db import models
from accounts.models import User

# Create your models here.
class SimilarFileUpload(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    imgfile = models.ImageField(null=True, upload_to="", blank=True)
    image_route = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class DeepExercise(models.Model):
    pk_id = pk_id = models.AutoField(db_column='pk_id', primary_key=True)
    content = models.CharField(db_column="content", max_length=200, blank=True, null=True)
    ex1 = models.CharField(db_column="ex1", max_length=150, blank=True, null=True)
    ex2 = models.CharField(db_column="ex2", max_length=150, blank=True, null=True)
    ex3 = models.CharField(db_column="ex3", max_length=150, blank=True, null=True)
    ex4 = models.CharField(db_column="ex4", max_length=150, blank=True, null=True)
    session_number = models.IntegerField(db_column="session_number", blank=True, null=True)
    answer = models.IntegerField(db_column="answer",blank=True, null=True)

    class Meta:
        db_table = 'deep_exercise'