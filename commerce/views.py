import inspect
from django.shortcuts import render

from app.views import get_user_from_session, send_error_mail
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

        try:
            item = Item.objects.get(itemId=itemId)
            # REVIEW: ALERT, prev code would only change one entry at a time, was this intended? 
            # RESPONSE: No 
            item.name = name or item.name
            item.itemId = itemId or item.itemId
            item.price = price or item.price
            item.size = size or item.size
        except Item.DoesNotExist as e:
            item = Item.objects.create(name=name, itemId=itemId, price=price, size=size)
        item.save()
        return r200("Item upserted!")

    except KeyError as e:
        # send_error_mail(inspect.stack()[0][3], request.data, e)
        print(e)
        return r500("Please send all the details")
    except Exception as e:
        # send_error_mail(inspect.stack()[0][3], request.data, e)
        print(e)
        return r500("Something failed")


@api_view(["POST"])
def upsertAddress(request):
    """
    ### adds or updates new address for a user \n Requires token
    """
    data = request.data
    if data:
        try:
            user=get_user_from_session(request)
            if user is None:
                return r500("User Not Found")
            userId=user.username
            dt_address = data["address"]
            dt_pinCode = data["pincode"]

            try:
                address= Address.objects.get(userId=userId)
                address.address=dt_address or address.address
                address.pincode=dt_pinCode or address.pincode
            except Address.DoesNotExist as e:
                address = Address.objects.create(
                    userId=userId, address=dt_address, pincode=dt_pinCode)
                
            address.save()

            return r200("address upserted")

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
    ### To get whether a user has atleast 1 address or not. \n Requires token
    """
    data = request.data
    if data:
        try:
            user=get_user_from_session(request)
            if user is None:
                return r500("User Not Found")
            userId=user.username

            try:
                address=Address.objects.get(userId=userId)
                return Response({"status": 200, "hasaddress": True, "address": address.address , "pincode":address.pincode})
            except Address.DoesNotExist as e:
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
    ### Call this to get all the addresses associated with a userId(email). \n Requires token
    """
    data = request.data
    if data:
        try:
            user=get_user_from_session(request)
            if user is None:
                return r500("User Not Found")
            userId=user.username
            try:
                db_adressess = Address.objects.get(userId=userId)
                return Response({"status": 200, "address": db_adressess.address , "pinCode": db_adressess.pincode })
            except Address.DoesNotExist as e:
                print(e)
                return r500("This user does not have any address associated with it.")

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
    #### Adds a new entry to the payment table. \n Requires token
    """
    data = request.data
    if data:
        try:
            tr_Id = data["transactionId"]
            itemId = data["itemId"]
            user=get_user_from_session(request)
            if user is None:
                return r500("User Not Found")
            userId=user.username

            try:
                Item.objects.get(itemId=itemId)
            except Item.DoesNotExist as e:
                return r500("Item not found. Please recheck the given Id")

            try:
                PaymentTable.objects.get(transactionId=tr_Id)
                return r500("transaction already made")
            except PaymentTable.DoesNotExist as e:
            
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
            try:
                Item.objects.get(itemId=itemId)
            except Item.DoesNotExist as e:
                return r500("Item not found. Please recheck the given Id")

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
