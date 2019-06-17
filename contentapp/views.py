# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from contentapp.models import UserSignup,UrlPostfixHistory,AboutUs,FakeRaters,Rating,EmailOTP,UserStoryTitle,UserPoem
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
from django.shortcuts import render
from django.shortcuts import render_to_response
from random import randint

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
            super_user_obj[0].email= email
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
        #if user.is_active==True:
        #   return Response(USER_ALREADY_REGISTERED,status=status.HTTP_200_OK)
        user.is_active = True
        user.save()
        user_detail = UserSignup.objects.get(email=email)
        user_detail.status = True
        user_detail.save()

        urlpost_fix = UrlPostfixHistory.objects.get(user_email=email)
        urlpost_fix.url_postfix_status = True
        urlpost_fix.save()
        context = {
            'username': user.username,
            'password': user.password,
            'admin_login': ADMIN_LOGIN,
            'user_profile': USER_PROFILE.format(urlpost_fix.url_postfix)
        }
        return render(request, 'index.html', context=context)
        #return Response(USER_REGISTERED,status=status.HTTP_200_OK)
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


@api_view(['GET'])
def home_page_detail(request):
    try:
        desktop_detail = [{"image_path":DESKTOP_COVER_IMAGE_4,"quote":HOME_QUOTE_1,"text_color":TEXT_COLORE_1},{"image_path":DESKTOP_COVER_IMAGE_3,"quote":HOME_QUOTE_4,"text_color":TEXT_COLORE_1},{"image_path":DESKTOP_COVER_IMAGE_9,"quote":HOME_QUOTE_2,"text_color":TEXT_COLOR_WHITE},{"image_path":DESKTOP_COVER_IMAGE_8,"quote":HOME_QUOTE_1,"text_color":TEXT_COLOR_WHITE}]
        mobile_detail = [{"image_path":MOBILE_COVER_IMAGE_3,"quote":HOME_QUOTE_4,"text_color":MOBILE_COLORE_1},{"image_path":MOBILE_COVER_IMAGE_4,"quote":MOBILE_QUOTE_1,"text_color":MOBILE_COLORE_1},{"image_path":MOBILE_COVER_IMAGE_9,"quote":MOBILE_QUOTE_2,"text_color":TEXT_COLOR_WHITE},{"image_path":MOBILE_COVER_IMAGE_6,"quote":HOME_QUOTE_3,"text_color":TEXT_COLOR_WHITE},{"image_path":MOBILE_COVER_IMAGE_1,"quote":MOBILE_QUOTE_1,"text_color":MOBILE_COLORE_1},{"image_path":MOBILE_COVER_IMAGE_2,"quote":MOBILE_QUOTE_1,"text_color":TEXT_COLOR_WHITE},{"image_path":MOBILE_COVER_IMAGE_7,"quote":MOBILE_QUOTE_1,"text_color":TEXT_COLOR_WHITE},{"image_path":MOBILE_COVER_IMAGE_5,"quote":MOBILE_QUOTE_1,"text_color":MOBILE_COLORE_1}]
        return Response({"desktop":desktop_detail,"mobile":mobile_detail},status=status.HTTP_200_OK)

    except Exception as error:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def rating_email(request):
    try:
        email = request.data['email']
        name = request.data['name']
        search_by = request.data['search_by']
        page_title = request.data['page_title']
        page_type = request.data['page_type']

        if page_type=="story":
           page_type_obj = UserStoryTitle.objects.get(search_by=search_by)

        elif page_type=="poem":
           page_type_obj = UserPoem.objects.get(search_by=search_by)

        author_email = page_type_obj.author.email
        if author_email==email:
           return Response(SELF_RATING, status=status.HTTP_302_FOUND)

        fake_obj = FakeRaters.objects.filter(email=email,status=True)
        if fake_obj:
           return Response(FAKE_USER, status=status.HTTP_302_FOUND)

        rating_queryset = Rating.objects.filter(rate_by=email,rated_title=search_by)
        if rating_queryset:
           return Response(ALREADY_RATED.format(page_title), status=status.HTTP_302_FOUND)

        # Generate random number for otp
        otp = random_with_N_digits(4)
        email_otp_obj = EmailOTP.objects.get_or_create(email=email)
        email_otp_obj[0].otp_number = otp
        email_otp_obj[0].save()

        name = name.split()[0]
        # sending Email using otp

        html_content = render_to_string(
                'mail_template.html', {'var_name': name.title(), 'body_content':SENT_EMAIL_WITH_OTP.format(otp,page_title.title())})
        send_email(SUBJECT_FOR_OTP, html_content, [email])

        return Response(SENT_OTP, status=status.HTTP_200_OK)

    except Exception as error:
        print("heyyyyyyyyyyyyyyyyyyyyyyyy",error)
        return Response(ABOUT_US,status=status.HTTP_404_NOT_FOUND)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


@api_view(['POST'])
def verify_otp(request):
    try:
        otp = request.data['otp']
        email = request.data['email']
        EmailOTP.objects.get(email=email,otp_number=otp)
        return Response(OTP_VALIDATED, status=status.HTTP_200_OK)

    except Exception as error:
        return Response(NOT_VALIDATE, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def rating_detail(request):
    try:
        otp = request.data['otp']
        email = request.data['email']
        name = request.data['name']
        search_by = request.data['search_by']
        star_value = request.data['star_value']
        page_title = request.data['page_title']
        comment = request.data['comment']
        page_type = request.data['page_type']
        EmailOTP.objects.get(email=email,otp_number=otp)
        rating_queryset = Rating.objects.filter(rate_by=email,rated_title=search_by)
        if rating_queryset:
           return Response(ALREADY_RATED.format(page_title), status=status.HTTP_302_FOUND)

        # insert star value in DB
        insert_star_value(star_value, page_type, search_by)

        rating_obj = Rating.objects.get_or_create(rate_by=email,rated_title=search_by)
        rating_obj[0].user_name = name
        rating_obj[0].rating_value = star_value
        rating_obj[0].comment = comment
        rating_obj[0].save()

        # calculate overall rating and save it
        calculate_overall_rating(page_type, search_by)

        return Response(RATING_SAVED.format(page_title.title()), status=status.HTTP_200_OK)

    except Exception as error:
        print("error---------------",error)
        return Response(OTP_ISSUE, status=status.HTTP_404_NOT_FOUND)

def insert_star_value(star_value, page_type, search_by):

     if page_type=="story":
          page_type_obj = UserStoryTitle.objects.get(search_by=search_by)

     elif page_type=="poem":
          page_type_obj = UserPoem.objects.get(search_by=search_by)

     if star_value == 1:
          page_type_obj.one_star_count = page_type_obj.one_star_count + 1
     elif star_value == 2:
          page_type_obj.two_star_count = page_type_obj.two_star_count + 1
     elif star_value == 3:
          page_type_obj.three_star_count = page_type_obj.three_star_count + 1
     elif star_value == 4:
          page_type_obj.four_star_count = page_type_obj.four_star_count + 1
     elif star_value == 5:
          page_type_obj.five_star_count = page_type_obj.five_star_count + 1

     page_type_obj.total_reviewer = page_type_obj.total_reviewer + 1
     page_type_obj.save()


def calculate_overall_rating(page_type, search_by):

     if page_type=="story":
          page_type_obj = UserStoryTitle.objects.get(search_by=search_by)

     elif page_type=="poem":
          page_type_obj = UserPoem.objects.get(search_by=search_by)

     one_star = page_type_obj.one_star_count * 1
     two_star = page_type_obj.two_star_count * 2
     three_star = page_type_obj.three_star_count * 3
     four_star = page_type_obj.four_star_count * 4
     five_star = page_type_obj.five_star_count * 5
     total_reviewer = page_type_obj.total_reviewer

     total = one_star+two_star+three_star+four_star+five_star
     total_rating = round(total/total_reviewer,1)

     one_star_avg = round(page_type_obj.one_star_count*100/total_reviewer,1)
     two_star_avg = round(page_type_obj.two_star_count*100/total_reviewer,1)
     three_star_avg = round(page_type_obj.three_star_count*100/total_reviewer,1)
     four_star_avg = round(page_type_obj.four_star_count*100/total_reviewer,1)
     five_star_avg = round(page_type_obj.five_star_count*100/total_reviewer,1)

     if (int(one_star_avg)+0.5)>one_star_avg:
        one_star_avg=int(one_star_avg)
     else:
        one_star_avg=int(one_star_avg)+1

     if (int(two_star_avg)+0.5)>two_star_avg:
        two_star_avg=int(two_star_avg)
     else:
        two_star_avg=int(two_star_avg)+1

     if (int(three_star_avg)+0.5)>three_star_avg:
        three_star_avg=int(three_star_avg)
     else:
        three_star_avg=int(three_star_avg)+1

     if (int(four_star_avg)+0.5)>four_star_avg:
        four_star_avg=int(four_star_avg)
     else:
        four_star_avg=int(four_star_avg)+1

     if (int(five_star_avg)+0.5)>five_star_avg:
        five_star_avg=int(five_star_avg)
     else:
        five_star_avg=int(five_star_avg)+1

     avg_list=[one_star_avg,two_star_avg,three_star_avg,four_star_avg,five_star_avg]
     avg_list.sort()
     highest_number=avg_list[-1]
     total_sum = sum(avg_list)

     if total_sum==100:
        pass
     else:
         difference = total_sum-100
         if highest_number==one_star_avg:
            one_star_avg=one_star_avg-difference
         elif highest_number==two_star_avg:
            two_star_avg=two_star_avg-difference
         elif highest_number==three_star_avg:
            three_star_avg=three_star_avg-difference
         elif highest_number==four_star_avg:
            four_star_avg=four_star_avg-difference
         elif highest_number==five_star_avg:
            five_star_avg=five_star_avg-difference

     page_type_obj.one_star_avg=one_star_avg
     page_type_obj.two_star_avg=two_star_avg
     page_type_obj.three_star_avg=three_star_avg
     page_type_obj.four_star_avg=four_star_avg
     page_type_obj.five_star_avg=five_star_avg
     page_type_obj.overall_rating=total_rating
     page_type_obj.save()
