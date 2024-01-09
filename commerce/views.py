import inspect
from django.shortcuts import render

from app.views import send_error_mail
from .models import *
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.request import Request, Empty
from resp import r200, r500
from rest_framework.decorators import api_view

# Create your views here.


@api_view(["POST"])
def upsertItem(request):
    # REVIEW: really cool name, I am stealing it for my projects thanks alonot!
    """
    #### updates an item if already exists otherwise adds it the db.
    """
    data = request.data
    if not data:
        return r500("No data recieved")

    try:
        print(data)
        name = data["name"]
        itemId = data["itemId"]
        price = data["price"]
        size = data["size"]

        item = Item.objects.filter(itemId=itemId).first()
        if item:
            # REVIEW: ALERT, prev code would only change one entry at a time, was this intended? 
            item.name = name or item.name
            item.itemId = itemId or item.itemId
            item.price = price or item.price
            item.size = size or item.size
        else:
            item = Item.objects.create(name=name, itemId=itemId, price=price, size=size)
        item.save()
        return r200("Item upserted!")

    except KeyError as e:
        # send_error_mail(inspect.stack()[0][3], request.data, e)
        print(e)
        return r500("Please send all the details")
    except Exception as e:
        send_error_mail(inspect.stack()[0][3], request.data, e)
        print(e)
        return r500("Something failed")


@api_view(["POST"])
def addAddress(request):
    """
    ### adds new address for a user
    """
    data = request.data
    if data:
        try:
            userId = data["userId"]
            address = data["address"]
            pinCode = data["pinCode"]

            if Address.objects.filter(address=address, userId=userId).first():
                return r500("Already added")

            address = Address.objects.create(
                userId=userId, address=address, pincode=pinCode
            )
            address.save()

            return r200("address added")

        except KeyError as e:
            # send_error_mail(inspect.stack()[0][3], request.data, e)
            print(e)
            return r500("Please send all the details")
        except Exception as e:
            # send_error_mail(inspect.stack()[0][3], request.data, e)
            print(e)
            return r500("Something failed")
    else:
        return r500("No data recievved")


@api_view(["POST"])
def hasAddress(request):
    """
    ### To get whether a user has atleast 1 address or not.
    """
    data = request.data
    if data:
        try:
            userId = data["userId"]

            if Address.objects.filter(userId=userId).first():
                return Response({"status": 200, "hasaddress": True})
            else:
                return Response({"status": 200, "hasaddress": False})

        except KeyError as e:
            # send_error_mail(inspect.stack()[0][3], request.data, e)
            print(e)
            return r500("Please send all the details")
        except Exception as e:
            # send_error_mail(inspect.stack()[0][3], request.data, e)
            print(e)
            return r500("Something failed")
    else:
        return r500("No data recieved")


@api_view(["POST"])
def getAddress(request):
    """
    ### Call this to get all the addresses associated with a userId(email)
    """
    data = request.data
    if data:
        try:
            userId = data["userId"]
            allAddresses = []

            db_adressess = Address.objects.filter(userId=userId).values()
            for address in db_adressess:
                allAddresses.append(
                    {"address": address["address"], "pinCode": address["pincode"]}
                )

            return Response({"status": 200, "addresses": allAddresses})

        except KeyError as e:
            # send_error_mail(inspect.stack()[0][3], request.data, e)
            print(e)
            return r500("Please send all the details")
        except Exception as e:
            # send_error_mail(inspect.stack()[0][3], request.data, e)
            print(e)
            return r500("Something failed")
    else:
        return r500("No data recieved")


@api_view(["POST"])
def makeTransaction(request):
    """
    #### Adds a new entry to the payment table.
    """
    data = request.data
    if data:
        try:
            tr_Id = data["transactionId"]
            itemId = data["itemId"]
            userId = data["userId"]

            if PaymentTable.objects.filter(transactionId=tr_Id).first():
                return r500("transaction already made")
            else:
                verified = False
                if userId.endswith("@smail.iitpkd.ac.in"):
                    verified = True
                payment = PaymentTable.objects.create(
                    transactionId=tr_Id, itemId=itemId, userId=userId, verified=verified
                )
                payment.save()

            return r200("payment saved")

        except KeyError as e:
            # send_error_mail(inspect.stack()[0][3], request.data, e)
            print(e)
            return r500("Please send all the details")
        except Exception as e:
            # send_error_mail(inspect.stack()[0][3], request.data, e)
            print(e)
            return r500("Something failed")
    else:
        return r500("No data recievved")


@api_view(["POST"])
def filterTransaction(request):
    """
    #### Filters all the transacctions corresponding to a particular itemId.
    """
    data = request.data
    if data:
        try:
            itemId = data["itemId"]
            allTrs = []

            trs = PaymentTable.objects.filter(itemId=itemId).values()
            for tr in trs:
                allTrs.append(
                    {"transactionId": tr["transactionId"], "userId": tr["userId"]}
                )

            return Response({"status": 200, "transactions": allTrs})

        except KeyError as e:
            # send_error_mail(inspect.stack()[0][3], request.data, e)
            print(e)
            return r500("Please send all the details")
        except Exception as e:
            # send_error_mail(inspect.stack()[0][3], request.data, e)
            print(e)
            return r500("Something failed")
    else:
        return r500("No data recievved")
