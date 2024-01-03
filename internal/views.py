from rest_framework.decorators import api_view
from app.models import *
from rest_framework.response import Response
from resp import r200, r500

# Create your views here.
@api_view(['GET'])
def getUnconfirmed(request):
    try:
        unconfirmed_users=set(EventTable.objects.exclude(transactionId="Internal Student").values_list('user_id'))
        print(unconfirmed_users)
        unconfirmed_list=[]
        for user in unconfirmed_users:
            user_id=user[0]

            events=EventTable.objects.filter(user_id=user_id)
            event_dict=dict()
            for event in events:
                if not event.verified:
                    event_dict[Event.objects.get(eventId=event.eventId).name]=event.transactionId
            
            user_name=Profile.objects.get(userId=user_id).username
            unconfirmed_list.append({user_name:event_dict})
        
        return Response(
            {
                "data":unconfirmed_list
            }
        )
    except Exception as e:
        return r500("Oopsie Doopsie")
    
@api_view(['GET'])
def getEventUsers(request):
    if request.method == "GET":
        events=[]
        try:
            allEvents=Event.objects.all()
            for event in allEvents:
                participantsId=set(EventTable.objects.filter(eventId=event.eventId).values_list('user_id'))
                participants=[]
                for id in participantsId:
                    user=Profile.objects.get(userId=id[0])
                    participants.append({
                        "name":user.username,
                        "email":user.email,
                        "phone":user.phone,
                    })
                events.append({
                    "name": event.name,
                    "participants":participants
                })


            print("Coreect")
            return Response({
                'status': 200,
                'data':["name","email","phone"],
                "events":events
            })
        except Exception as e:
            return r500("Opps!! Unable to complete the request!!!")
    

@api_view(['POST'])
def verifyTR(request):
    try:
        if request.data == None:
            return r500("Invalid Form")
        
        data=request.data
        print("print:",data)

        inputTRId=data['TransactionId'].strip()
        try:
            event=EventTable.objects.get(transactionId=inputTRId)
            event.verified = True
            return Response({
                'status' : 200,
                'verified': True
            })
        except Exception as e:
            return Response({
                'status':404,
                'verified': False,
                'msg':"Not found in our db"
            })




    except Exception as e:
        return Response({
                'status':400,
                'verified': False,
                'msg':"Opps!! Unable to complete the request!!!"
            })
    

@api_view(['POST'])
def addEvent(request):
    try:
        data=request.data
        if data == None:
            return r500("Please send some info about the event")
        event = Event.objects.create(
            eventId=data["id"],
            name=data["name"],
            fee=data["fees"],
            minMember=data["minMember"],
            maxMember=data["maxMember"]
        )
        event.save()
        return r200("Event saved successfully")
    
    except Exception as e:
        print(e)
        return r500("Something went wrong.")
