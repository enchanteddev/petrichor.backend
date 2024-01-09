from django.db import models

# Create your models here.

class Item(models.Model):
    name=models.TextField()
    itemId=models.CharField(max_length=10,default="",primary_key=True)
    price=models.IntegerField(default=0)
    size=models.TextField()
    def __str__(self) -> str:
        return self.name

class PaymentTable(models.Model):
    transactionId=models.TextField()
    itemId=models.CharField(null=True,max_length=10)
    userId=models.EmailField()
    verified=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.userId+":\t"+self.itemId

class Address(models.Model):
    userId=models.EmailField()
    address=models.TextField()
    pincode=models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.address+"\n"+str(self.pincode)