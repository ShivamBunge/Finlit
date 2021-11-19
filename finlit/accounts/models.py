from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, IntegerField
from django.dispatch import receiver
from django.db.models.signals import post_save

from profession.models import Profession
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    current_job=models.CharField(default="NA",max_length=50)
    prof=models.ForeignKey(Profession,on_delete=models.CASCADE,null=True)
    # prtf=models.ForeignKey(portfolio,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    # instance.profile.save()

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()


class portfolio(models.Model):
    #-------- DO CHANGES HERE--------------------
    # player=models.ForeignKey(Profession,on_delete=models.CASCADE)
    player=models.OneToOneField(User,on_delete=models.CASCADE)
    stocks=models.IntegerField(default=00)
    mutual_funds=models.IntegerField(default=00)
    fds=models.IntegerField(default=00)
    gold=models.IntegerField(default=00)
    loans=models.IntegerField(default=00)

    pg_no=models.IntegerField(default=0)
    total_prtf_val=models.IntegerField(default=00)
    
    balance=models.IntegerField(default=100)
    
    def __str__(self):
        return f'{self.player.username} Portfolio'
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

@receiver(post_save,sender=User)
def create_portfolio(sender,instance,created,**kwargs):
    if created:
        portfolio.objects.create(player=instance)
    # instance.profile.save()

@receiver(post_save,sender=User)
def save_portfolio(sender,instance,**kwargs):
    instance.portfolio.save()