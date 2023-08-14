from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile
from userapi import settings
from .tokens import generate_token
from django.core.mail import EmailMessage, send_mail
# Create your views here.
def home(request):
    return HttpResponse('This is the homepage!')
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        data = request.data
        username = data['username']
        email = data['email']
        pass1 = data['password']
        phone = data['phone']
        college = data['college']
        year = data['year']
        # print(username, email, pass1, pass2)
        # checks for same username
        if User.objects.filter(username=username).first():
            return Response(
                {'status': 404,
                    "registered": "false",
                    'message': "Username already registered",
                    "username": username
                    }
            )

        # checks if the username exists
        elif User.objects.filter(email=email).first():
            return Response({
                'status': 404,
                "registered": "false",
                'message': "Email already registered",
                "username": username
            })

        # Creates a new user and adds it to the profile with a new CA_code
        else:
            new_user = User.objects.create_user(username, email, pass1)

            # Not activating the user unless the confirmation mail is opened
            new_user.is_active = False
            new_user.save()

            ca_profile = Profile.objects.create(username=username, email=email, phone=phone, college=college, year=year)
            ca_code = ca_profile.CA
            ca_profile.save()

            # Confimation link mail
            current_site = get_current_site(request)
            email_subject = "Petrichor Fest - Campus Ambassador Programme Confirmation"
            confirmation_message = render_to_string('confirmation_email.html',
                                                    {
                                                        'username': username,
                                                        'domain': current_site.domain,
                                                        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                                                        'token': generate_token.make_token(new_user)
                                                    })   # add a html template
            email_cnf = EmailMessage(
                email_subject,
                confirmation_message,
                settings.EMAIL_HOST_USER,
                [new_user.email],
            )
            email_cnf.fail_silently = False
            print(settings.EMAIL_BACKEND, "a")
            email_cnf.send()
            print("mail sent to", new_user.email)

            # Sending Email with CA code



            return Response({
                'status': 200,
                "registered": "true",
                'message': "Success",
                "username": username
            })

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        data = request.data
        username = data['username']
        password = data['password']
        my_user = authenticate(username = username, password = password)
        if my_user is not None:
            login(request, my_user)
            profile = Profile.objects.get(username=username)
            return Response({
                "ok": "true",
                "CA": profile.CA,
                "username": profile.username,
                "registrations": 0
            })
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


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
        # print(new_user.username)
        # print(uid)
        # print(token)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_user = None

    if new_user is not None and generate_token.check_token(new_user, token):

        new_user.is_active = True
        new_user.save()
        userprof = Profile.objects.get(username=new_user.username)
        userprof.generate_CA()
        # print(userprof.CA)
        userprof.save()
        login(request, new_user)
        subject = "Welcome to Petrichor's Campus Ambassador Programme"
        message = f"Hello there, {new_user.username} \nPlease click the following link to activate your CA account {userprof.CA}"
        from_mail = settings.EMAIL_HOST_USER
        to_mail_ls = [new_user.email]

        send_mail(subject, message, from_mail, to_mail_ls, fail_silently=True)
        # return Response(
        #     {
        #         "logged-in": "True",
        #         "message": "Your email has been confirmed"
        #     }
        # )
        return render(request, 'success.html')
    else:
        # return Response(
        #     {
        #         "logged-in": "False",
        #         "message": "Account was not verified, activation failed"
        #     }
        # )
        return redirect(request, 'failure.html')


def mailtest(request):
    current_site = get_current_site(request)
    email_subject = "Petrichor Fest - Campus Ambassador Programme Confirmation"
    confirmation_message = render_to_string('confirmation_email.html',
                                            {
                                                'username': 'hello',
                                                'domain': current_site.domain,
                                                'uid': "urlsafe_base64_encode(force_bytes('new_user.pk'))",
                                                'token': "generate_token.make_token('new_user')"
                                            })   # add a html template
    email_cnf = EmailMessage(
        email_subject,
        confirmation_message,
        settings.EMAIL_HOST_USER,
        ['112201015@smail.iitpkd.ac.in'],
    )
    print(email_cnf)
    email_cnf.fail_silently = False
    # print(settings.EMAIL_BACKEND, "a")
    email_cnf.send()
    print('email sent to', '112201015@smail.iitpkd.ac.in')

    return HttpResponse("email send to")