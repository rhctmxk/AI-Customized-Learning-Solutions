from django.db import models

# Create your models here.



class Data_sum_detail1(models.Model):
    pk_id = models.AutoField(db_column="PK_ID", primary_key=True)
    job = models.CharField(db_column="JOB", max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'data_sum_detail1'


class Technology_korea(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)
    fk_detail1 = models.ForeignKey(Data_sum_detail1, models.DO_NOTHING, blank=True, null=True, db_column="FK_DETAIL1")
    license = models.CharField(db_column="QUAL", max_length=50, blank=True, null=True)
    summary = models.CharField(db_column="SUMMARY", max_length=10000, blank=True, null=True)
    activate = models.IntegerField(blank=True, null=True, default=0)
    class Meta:
        db_table = 'technology_korea'


class Technology_other(models.Model):
    pk_id = models.AutoField(db_column='PK_ID', primary_key=True)
    fk_detail1 = models.ForeignKey(Data_sum_detail1, models.DO_NOTHING, blank=True, null=True, db_column="FK_DETAIL1")
    license = models.CharField(db_column="QUAL", max_length=50, blank=True, null=True)
    summary = models.CharField(db_column="SUMMARY", max_length=10000, blank=True, null=True)
    activate = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'technology_other'

class License_raking(models.Model):
    license = models.CharField(max_length=50, blank=True, null=True)
    count = models.IntegerField(blank=True, default=0)

# class License_info(models.Model):
#     pk_id = models.AutoField(db_column='PK_ID', primary_key=True)
#     license_korea = models.ForeignKey(Technology_korea, models.DO_NOTHING, blank=True, null=True)
#     license_other = models.ForeignKey(Technology_other, models.DO_NOTHING, blank=True, null=True)
