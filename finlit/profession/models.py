from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, IntegerField
from django.dispatch import receiver
from django.db.models.signals import post_save


# from accounts.models import Profile
# Create your models here.

class Profession(models.Model):
    class Risk(models.IntegerChoices):
        LOw=1
        MEDIUM=2
        HIGH=3
    # prof_user = models.OneToOneField(Profile,on_delete=models.CASCADE)


    prof_name=models.CharField(max_length=30)
    prof_img= models.ImageField(upload_to='pics')
    prof_desc = models.TextField()
    income = models.BigIntegerField()
    expend = models.BigIntegerField()
    risk= models.IntegerField(choices=Risk.choices)
    progress= models.IntegerField(choices=Risk.choices)
    def __str__(self):
        return f'{self.prof_name}'
    




    
