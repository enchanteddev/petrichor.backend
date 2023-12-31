from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User=get_user_model()


class Institute(models.Model):
    institutionType = models.CharField(max_length=255, null=True)
    instiName = models.CharField(unique=True, max_length=255)
    def __str__(self):
        return self.instiName


class Profile(models.Model):
    # objects = None

    # userId=models.IntegerField()
    username = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    phone = models.CharField(max_length=13)
    instituteID = models.CharField(null=True, max_length=255)
    gradYear = models.IntegerField(default=6969)
    stream = models.CharField(null=True, max_length=10)


    def __str__(self):
        return self.username
    

class Event(models.Model):
    eventId=models.CharField(max_length=10,default="", primary_key=True)
    name=models.CharField(max_length=20,default="")
    fee = models.IntegerField(default=0)
    minMember = models.IntegerField(default=1)
    maxMember = models.IntegerField(default=1)


sep = '\n'
class EventTable(models.Model):
    eventId=models.CharField(max_length=10,null=True)
    emails = models.TextField(default="")
    transactionId=models.CharField(max_length=25, primary_key=True)
    verified=models.BooleanField()

    @staticmethod
    def serialise_emails(emails: list[str]):
        return sep.join(emails)
    
    def get_emails(self) -> list[str]:
        return self.emails.split(sep)
