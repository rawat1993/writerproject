# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from contentapp.models import UserSignup,UrlPostfixHistory,AboutUs
from contentapp.serializers import UserSignup_Serializer
from django.contrib.auth.models import User
from .constants import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.decorators import api_view
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from contentapp.user_profile_views import append_baseUrl

def send_email(subject, send_message, toUser):
    """
    Send email function
    """

    text_content = strip_tags(send_message)
    msg = EmailMultiAlternatives(
        subject, text_content, 'writercreativity612@gmail.com', toUser)
    msg.attach_alternative(send_message, "text/html")
    msg.send()


def generate_confirmation_token(email):
    """
    Generate token using user Email
    """
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt=SALT)


def confirm_token(token, expiration=EMAIL_TOKEN_EXP_IN_SECONDS):
    """
    Confirm token and check for expiration token for 3600 seconds
    """
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=SALT, max_age=expiration)
        return email
    except Exception as e:
        return False

class UserSignupView(APIView):

    def post(self,request):
        try:
            full_name = (request.data).get('username')
            email = (request.data).get('email')
            password = (request.data).get('password')
            url_postfix = (request.data).get('url_postfix')
            user_obj = UserSignup.objects.get_or_create(email=email)
            super_user_obj = User.objects.get_or_create(username=email)
            if super_user_obj[1]==False:
                if super_user_obj[0].is_active==True:
                   return Response(USER_EMAIL_ALREADY_EXISTS,status=status.HTTP_200_OK)

            user_obj[0].full_name = full_name
            user_obj[0].save()

            token = generate_confirmation_token(email)
            html_content = render_to_string(
                'mail_template.html', {'var_name': full_name.title(), 'body_content': EMAIL_CONTENT, 'activation_link': ACTIVATION_LINK.format(token),'username':USER_NAME.format(email),'password':PASSWORD.format(password),'admin_login':ADMIN_LOGIN,'user_profile':USER_PROFILE.format(url_postfix)})

            # create objects in User model to admin login
            super_user_obj[0].set_password(password)
            super_user_obj[0].is_superuser = True
            super_user_obj[0].is_active = False
            super_user_obj[0].is_staff = True
            super_user_obj[0].save()

            send_email(EMAIL_SUBJECTS, html_content, [email])

            # UrlPostfix entry
            availability = UrlPostfixHistory.objects.filter(url_postfix=url_postfix,url_postfix_status=True)
            if availability:
               return Response(POSTFIX_NOT_AVAILABLE,status=status.HTTP_302_FOUND)

            postfix_obj = UrlPostfixHistory.objects.get_or_create(user_email=email)
            postfix_obj[0].url_postfix = url_postfix
            postfix_obj[0].save()
            return Response(MAIL_SUCCESSFULLY_SENT,status=status.HTTP_201_CREATED)

        except Exception as error:
            import os,sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno,error)
            return Response(MAIL_FAILD,status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def user_activation(request):
    try:
        token = request.GET['token']
        if confirm_token(token) == False:
            return Response(TOKEN_EXPIRE, status=status.HTTP_408_REQUEST_TIMEOUT)
        email = confirm_token(token)

        user = User.objects.get(username=email)
        if user.is_active==True:
           return Response(USER_ALREADY_REGISTERED,status=status.HTTP_200_OK)
        user.is_active = True
        user.save()
        user_detail = UserSignup.objects.get(email=email)
        user_detail.status = True
        user_detail.save()

        urlpost_fix = UrlPostfixHistory.objects.get(user_email=email)
        urlpost_fix.url_postfix_status = True
        urlpost_fix.save()
        return Response(USER_REGISTERED,status=status.HTTP_200_OK)
    except Exception as error:
        return Response(USER_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def url_postfix_availability(request):
    try:
        url_postfix = request.GET['url_postfix']
        availability = UrlPostfixHistory.objects.filter(url_postfix=url_postfix,url_postfix_status=True)
        if availability:
           return Response(POSTFIX_NOT_AVAILABLE,status=status.HTTP_302_FOUND)

        return Response(AVAILABLE,status=status.HTTP_200_OK)
    except Exception as error:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def about_us_page(request):
    try:
        about_us = AboutUs.objects.all()
        data = append_baseUrl(about_us,"about-us")
        return Response({"data":data},status=status.HTTP_200_OK)

    except Exception as error:
        print("heyyyyyyyyyyyyyyyyyyyyyyyy",error)
        return Response(ABOUT_US,status=status.HTTP_404_NOT_FOUND)




