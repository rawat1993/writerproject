# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from contentapp.models import UserSignup,UrlPostfixHistory
from contentapp.serializers import UserSignup_Serializer
from django.contrib.auth.models import User
from .constants import *
from django.core.mail import send_mail
from rest_framework.decorators import api_view

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

            # create objects in User model to admin login
            super_user_obj[0].set_password(password)
            super_user_obj[0].is_superuser = True
            super_user_obj[0].is_active = False
            super_user_obj[0].is_staff = True
            super_user_obj[0].save()

            # UrlPostfix entry
            postfix_obj = UrlPostfixHistory.objects.get_or_create(user_email=email)
            postfix_obj[0].url_postfix = url_postfix
            postfix_obj[0].save()

            send_mail(EMAIL_SUBJECTS,EMAIL_CONTENT.format(full_name,email), 'rawatajay977@gmail.com', [email])
            return Response(MAIL_SUCCESSFULLY_SENT,status=status.HTTP_201_CREATED)
        except Exception as error:
            import os,sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)           
            return Response(MAIL_FAILD,status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def user_activation(request):
    try:
        email = request.GET['token']
        user = User.objects.get(username=email)
        if user.is_active==True:
           return Response(USER_ALREADY_REGISTERED,status=status.HTTP_200_OK)
        user.is_active = True
        user.save()
        user_detail = UserSignup.objects.get(email=email)
        user_detail.status = True
        user_detail.save()
        return Response(USER_REGISTERED,status=status.HTTP_200_OK)
    except Exception as error:
        return Response(USER_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def url_postfix_availability(request):
    try:
        url_postfix = request.GET['url_postfix']
        availability = UrlPostfixHistory.objects.filter(url_postfix=url_postfix)
        if availability:
           return Response(POSTFIX_NOT_AVAILABLE,status=status.HTTP_302_FOUND)

        return Response(AVAILABLE,status=status.HTTP_200_OK)
    except Exception as error:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)






