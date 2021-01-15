from django.db import connections
from django.db import models
# Create your models here.

'''lass Movietitles(models.Model):   
    titleid = models.CharField(max_length=100)
    class Meta:
        db_table = "titlebasics"
'''

class Titleratings(models.Model):
    #tconst = models.CharField(db_column='tconst', db_index=True, primary_key=False, max_length=15, blank=True, null=True, unique=True)  # Field name made lowercase.
    titleid = models.IntegerField(db_column='titleid', db_index=True, primary_key=False, blank=True, null=True, unique=True)  # Field name made lowercase.
    averagerating = models.FloatField(db_column='averageRating', db_index=True, blank=True, null=True)  # Field name made lowercase.
    numvotes = models.IntegerField(db_column='numVotes', db_index=True, blank=True, null=True)  # Field name made lowercase.
  
    class Meta:
        managed = False
        db_table = 'titleratings'

class Titlebasics(models.Model):
    #tconst1 = models.CharField(db_column='tconst', primary_key=False, max_length=15, blank=True, null=True)  # Field name made lowercase.
    #ratings = models.ForeignKey(Titleratings,on_delete=models.DO_NOTHING, db_index=True, db_column='tconst', to_field='tconst')
    ratings = models.ForeignKey(Titleratings,on_delete=models.DO_NOTHING, db_index=True, db_column='titleid', to_field='titleid')
    titletype = models.CharField(db_column='titleType', max_length=15, blank=True, null=True)  # Field name made lowercase.
    originaltitle = models.TextField(db_column='originalTitle', blank=True, null=True)  # Field name made lowercase.
    startyear = models.TextField(db_column='startYear', blank=True, null=True)  # Field name made lowercase.
    genres = models.TextField(db_column='genres', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'titlebasics'


class watchedmovie(models.Model):
    titleid = models.IntegerField(db_column='titleid', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    userid = models.CharField(db_column='userid', max_length=15, blank=True, null=True)
    watched = models.CharField(db_column='watched', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recommended = models.CharField(db_column='recommended', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'watchedcontent'