from django.db import models
from accounts.models import User

# Create your models here.
# pk_id = models.AutoField(db_column='PK_ID', primary_key=True)
# user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id')
class PREVIOUS_EXERCISE_SUMMARY(models.Model):
    PK_ID = models.AutoField(db_column="PK_ID", primary_key=True)
    PRE_EXE_CLASS = models.IntegerField(db_column="PRE_EXE_CLASS", blank=True, null=True)
    PRE_EXE_YEAR = models.IntegerField(db_column="PRE_EXE_YEAR", blank=True, null=True)
    PRE_EXE_NUMBER = models.IntegerField(db_column="PRE_EXE_NUMBER", blank=True, null=True)
    PRE_EXE_SUBJECT = models.IntegerField(db_column="PRE_EXE_SUBJECT", blank=True, null=True)

    class Meta:
        db_table = 'previous_exercise_summary'

class PREVIOUS_EXERCISE_FIGURE_TABLE(models.Model):
    PK_ID = models.AutoField(db_column="PK_ID", primary_key=True)
    PRE_EXE_FIG_TAB_FIGURE = models.CharField(max_length=100, blank=True, null=True)
    PRE_EXE_FIG_TAB_FIGURE_PATH = models.CharField(db_column='PRE_EXE_FIG_TAB_FIGURE_PATH', max_length=300, blank=True, null=True)
    FK_PREVIOUS_EXERCISE_QUES = models.IntegerField(db_column='FK_PREVIOUS_EXERCISE_QUES', blank=True, null=True)
    FK_PREVIOUS_EXERCISE_EXAM = models.IntegerField(db_column='FK_PREVIOUS_EXERCISE_EXAM', blank=True, null=True)

    class Meta:
        db_table = 'previous_exercise_figure_table'


class PREVIOUS_EXERCISE_EXAM(models.Model):
    PK_ID = models.AutoField(db_column="PK_ID", primary_key=True)
    PRE_EXAM_NUM = models.IntegerField(blank=True, null=True)
    PRE_EXAM_SUBSTANCE = models.CharField(max_length=100, blank=True, null=True)
    PRE_EXAM_FIGURE = models.IntegerField(blank=True, null=True)
    FK_PREVIOUS_EXERCISE_QUES = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'previous_exercise_exam'


class PREVIOUS_EXERCISE_QUES(models.Model):
    PK_ID = models.AutoField(db_column="PK_ID", primary_key=True)
    PRE_EXE_QUES_NUM = models.IntegerField(blank=True, null=True)
    PRE_EXE_QUES_DIFFICULTY = models.CharField(max_length=2, blank=True, null=True)
    PRE_EXE_QUES_QUESTION = models.CharField(max_length=500, blank=True, null=True)
    PRE_EXE_QUES_FIGURE = models.IntegerField(blank=True, null=True)
    FK_PREVIOUS_EXERCISE_SUMMARY = models.IntegerField(blank=True, null=True)
    ANSWER_RATE = models.IntegerField(default=0)  # 정답률
    ANSWER = models.ForeignKey(PREVIOUS_EXERCISE_EXAM, models.DO_NOTHING, blank=True, null=True, db_column='ANSWER')

    class Meta:
        db_table = 'previous_exercise_ques'



class PREVIOUS_EXERCISE_EXAM_ANSWER(models.Model):
    SELECT = models.IntegerField(null=True, blank=True)
    DIVISION = models.IntegerField(null=True, blank=True)
    QUE_NUM = models.IntegerField(null=True, blank=True)
    QUE_ID = models.IntegerField(null=True, blank=True)
    USER_ID = models.CharField(max_length=30, null=True, blank=True)
    ANSWER_NUM = models.IntegerField(null=True, blank=True)
    ANSWER_CHECK = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'previous_exercise_exam_answer'

        #1 : 레벨
        #2 : 기출
        #3 : 난이도별


class PREVIOUS_EXERCISE_EXAM_RESULT(models.Model):
    SELECT = models.IntegerField(null=True, blank=True)
    DIVISION = models.IntegerField(null=True, blank=True)
    USER_ID = models.CharField(max_length=30, null=True, blank=True)
    QUE_COUNT = models.IntegerField(null=True, blank=True)
    ANSWER_COUNT = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'previous_exercise_exam_result'

class WeekScore(models.Model):
    week = models.CharField(max_length=30, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'WeekScore'

class MonthScore(models.Model):
    month = models.CharField(max_length=30, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'MonthScore'