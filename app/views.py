from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request, Empty
from resp import r500, r200
from .models import *
from userapi import settings
from django.core.mail import send_mail
# Create your views here.

def home(request):
    return HttpResponse('This is the homepage!')

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        data = request.data
        username = data['username'].strip()
        email = data['email']
        pass1 = data['password']
        phone = data['phone']
        insti_name = data['college']
        gradyear = data['gradyear']
        insti_type = data['institype']
        stream = data['stream']
        
        if User.objects.filter(email=email).first():
            return Response({
                'status': 404,
                "registered": False,
                'message': "Email already registered",
                "username": username
            })


        else:
            new_user = User(username=email)
            new_user.set_password(pass1)
            new_user.is_active = True
            new_user.save()
            

            institute = Institute.objects.get_or_create(instiName=insti_name, institutionType=insti_type)[0]
            # institute = Institute.objects.get(instiName=instituteID)

            print(institute.pk)


            user_profile = Profile.objects.create(username=username, 
                                                  email=email,
                                                  phone=phone,
                                                  instituteID=institute.pk,
                                                  gradYear=gradyear,
                                                  stream=stream)
            user_profile.save()

            return Response({
                'status': 200,
                "registered": True,
                'message': "Success",
                "username": username
            })


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':

        if request.data is None:
            return r500("invalid form")
        data=request.data

        username = data['username'].strip()
        print(username)
        password = data['password']
        print(password)
        my_user = authenticate(username = username, password = password)
        if my_user is not None:
            login(request, my_user)
            profile = Profile.objects.get(email=username)
            print("OK")
            request.session.set_test_cookie()
            num_visits = request.session.get( 'num_visits', 0)
            request.session ['num_visits'] = num_visits + 1
            return Response({
                "ok": True,
                "username": profile.username,
                "registrations": 0
            })
        print("Failed")
        return Response({
            "message": "The username or password is incorrect",
            "logged-in": "false"
        })

@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response(
        {
            "logged-in": "false",
            "message": "User has logged out"
        }
    )
    # return redirect('login')

@api_view(['POST'])
def getUserInfo(request):
    user = get_user_from_session(request)
    if user:
        print("Passed",user,"p")
        profileUser=Profile.objects.get(email=user)
        if profileUser:
            response={
                "username":profileUser.username,
                "email":profileUser.email,
                "phone":profileUser.phone,
                "instituteID":profileUser.instituteID,
                "gradyear":profileUser.gradYear,
                "stream":profileUser.stream
            } 
            events=[]
            eventEntries=EventTable.objects.all()
            for eventEntry in eventEntries:
                if str(user) in eventEntry.emails:
                    events.append({"eventId":eventEntry.eventId,"status":eventEntry.verified})
            response["events"]=events
            return Response({
                "status":200,
                "response":response
                })
    else:
        print("Auth failed")
        return Response({
            "status":200,
            "response":{
                "username":"alonot",
                "email":"csk1@gmail.com",
                "phone":"1221211221",
                "instituteID":"11222",
                "college":"IIT PKD",
                "gradyear":2029,
                "stream":"Science",
                "events":[{"eventId":"TP00","status":"Payment Verified"},
                          {"eventId":"WP02","status":"Payment Pending"}]
            }
        })
        return Response({
            "status":404,
            "response":None
        })


def get_user_from_session(request):
    user = get_user(request)    
    if user and user.is_authenticated:
        return user
    else:
        return None

@api_view(['POST'])
def whoami(request: Request):
    user = get_user_from_session(request)
    return Response({
        'whoami': user.username if user else None  # type: ignore
    })


@login_required
@api_view(['POST'])
def apply_event_paid(request: Request):
    data=request.data
    if data is None:
        return r500("invalid form")
    try:
        user=get_user_from_session(request)
        if user is None:
            return r500('login')
        user_email = user.username # type: ignore
        participants = data['participants'] # type: ignore
        event_id = data['eventID'].strip() # type: ignore
        transactionId = data['transactionId'].strip() # type: ignore

    except KeyError:
        return r500("participants, eventid and transactionId required. send all.'")
# try:
    verified=False
    if user_email.endswith("smail.iitpkd.ac.in"):
        verified=True
        transactionId="IIT Palakkad Student"
        
    eventTableObject = EventTable.objects.create(eventId=event_id,
                                                 emails=EventTable.serialise_emails(participants), #type: ignore
                                                 transactionId=transactionId,verified=verified)
    eventTableObject.save()
    return r200("Event applied")
    # except Exception:
    #     print(user_id,event_id,transactionId,verified)
    #     return r500("Oopsie Doopsie")


@login_required
@api_view(['POST'])
def apply_event_free(request):
    data=request.data
    if data is None:
        return r500("invalid form")
    try:
        user=get_user_from_session(request)
        if user is None:
            return r500('login')
        user_email = user.username # type: ignore
        participants = data['participants'] # type: ignore
        event_id = data['eventId'].strip() # type: ignore

    except KeyError:
        return r500("participants and eventid required. send both.'")

    transactionId = None
    if user_email.endswith("smail.iitpkd.ac.in"):
        transactionId="IIT Palakkad Student"
        
    eventTableObject = EventTable.objects.create(eventId=event_id,
                                                 emails=EventTable.serialise_emails(participants), #type: ignore
                                                 transactionId=transactionId, verified=True)
    eventTableObject.save()
    return r200("Event applied")


@login_required # limits the calls to this function ig
@api_view(['POST'])
def get_event_data(request):
    data=request.data
    if data is None:
        return r500("invalid form")
    try:
        event_id = data["eventID"]
    except KeyError:
        return r500("Send an eventID")
    
    event = Event.objects.filter(eventId = event_id).first()
    if event is None:
        return r500(f"Invalid Event ID = {event_id}")
    return Response({
        "name": event.name,
        "fee": event.fee,
    })


@api_view(['POST'])
def send_grievance(request: Request):
    try:
        data = request.data
        if isinstance(data, Empty) or data is None:
            return r500("Invalid Form")
        
        name = data['name'] # type: ignore
        email = data['email'] # type: ignore
        content = data['content'] # type: ignore

        send_mail(
            subject=f"WEBSITE MAIL: Grievance from '{name}'",
            message=f"From {name} ({email}).\n\n{content}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["112201015@smail.iitpkd.ac.in", "petrichor@iitpkd.ac.in"]
        )
        print("grievance email sent")
        return Response({
                'status':200,
                'success': True
            })

    except Exception as e:
        return Response({
                'status':400,
                'success': False
            })