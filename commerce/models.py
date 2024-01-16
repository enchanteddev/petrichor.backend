from django.db import models

# Create your models here.

class Item(models.Model):
    name=models.TextField()
    itemId=models.CharField(max_length=10,default="",primary_key=True)
    price=models.IntegerField(default=0)
    size=models.TextField()
    def __str__(self) -> str:
        return self.name

"""
ID structure:
first letter: M - Merch
              A - Accom
              X - Xtras

second letter: T - Tshirt
(for merch)    H - Hoodie
               Z - Zippie
               C - Cap
               
a number at the end starting from 0, increases in digits if req.
"""
class PaymentTable(models.Model):
    transactionId=models.TextField(primary_key=True)
    itemId=models.CharField(max_length=10,default="") # WHY WAS IT NULL = TRUE !?
    userId=models.EmailField()
    verified=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.userId+":\t"+self.itemId

class Address(models.Model):
    userId=models.EmailField(primary_key=True)
    address=models.TextField()
    pincode=models.IntegerField(default=-1)

    def __str__(self) -> str:
        return self.address+"\n"+str(self.pincode)