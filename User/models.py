from ast import mod
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class accountsCheck(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    crated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class instaAccounts(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    is_client = models.BooleanField(default=False)

class comparison(models.Model):
    client = models.ForeignKey(instaAccounts,on_delete=models.CASCADE,related_name="client")
    comparison_with = models.ForeignKey(instaAccounts,on_delete=models.CASCADE,related_name="comparison_with")

class ChannelSelector(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    channel= models.CharField(max_length=40)