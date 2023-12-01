from django.db import models

# Create your models here.

class Password(models.Model):
    title = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password =  models.CharField(max_length=50)

    class Meta():
        db_table = 'passwords'

class Media(models.Model):
    media = models.ImageField()
    caption = models.CharField(max_length=50)

    class Meta():
        db_table = 'media'
