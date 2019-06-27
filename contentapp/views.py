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
from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone
# from background_task import background
from contentapp.tasks import sent_notictaion_email_to_author

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
        page_type = request.GET.get('page_type',None)
        if page_type=="term":
           about_us = AboutUs.objects.filter(about_us='terms-conditions')
        else:
           about_us = AboutUs.objects.filter(about_us='about-us')
        data = append_baseUrl(about_us,"about-us")
        return Response({"data":data, "writer_listing_pag_link":LINK_NAME_FOR_WRITERS_LISTING_PAGE},status=status.HTTP_200_OK)

    except Exception as error:
        print("heyyyyyyyyyyyyyyyyyyyyyyyy",error)
        return Response(ABOUT_US,status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def home_page_detail(request):
    try:
        desktop_detail = [{"image_path":DESKTOP_COVER_IMAGE_4,"quote":HOME_QUOTE_1,"text_color":TEXT_COLORE_1},{"image_path":DESKTOP_COVER_IMAGE_3,"quote":HOME_QUOTE_5,"text_color":TEXT_COLORE_1},{"image_path":DESKTOP_COVER_IMAGE_9,"quote":HOME_QUOTE_4,"text_color":TEXT_COLOR_WHITE},{"image_path":DESKTOP_COVER_IMAGE_8,"quote":HOME_QUOTE_6,"text_color":TEXT_COLOR_WHITE}]
        mobile_detail = [{"image_path":MOBILE_COVER_IMAGE_4,"quote":MOBILE_QUOTE_1,"text_color":MOBILE_COLORE_1},{"image_path":MOBILE_COVER_IMAGE_3,"quote":HOME_QUOTE_5,"text_color":MOBILE_COLORE_1},{"image_path":MOBILE_COVER_IMAGE_9,"quote":HOME_QUOTE_4,"text_color":TEXT_COLOR_WHITE},{"image_path":MOBILE_COVER_IMAGE_6,"quote":HOME_QUOTE_3,"text_color":TEXT_COLOR_WHITE},{"image_path":MOBILE_COVER_IMAGE_7,"quote":MOBILE_QUOTE_3,"text_color":TEXT_COLOR_WHITE},{"image_path":MOBILE_COVER_IMAGE_5,"quote":HOME_QUOTE_6,"text_color":MOBILE_COLORE_1}]
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
        return Response(MAIL_FAILD,status=status.HTTP_404_NOT_FOUND)

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
        subject = request.data['subject']
        EmailOTP.objects.get(email=email,otp_number=otp)
        rating_queryset = Rating.objects.filter(rate_by=email,rated_title=search_by)
        if rating_queryset:
           return Response(ALREADY_RATED.format(page_title.title()), status=status.HTTP_302_FOUND)

        # insert star value in DB
        insert_star_value(star_value, page_type, search_by)

        rating_obj = Rating.objects.get_or_create(rate_by=email,rated_title=search_by)
        rating_obj[0].user_name = name
        rating_obj[0].rating_value = star_value
        rating_obj[0].comment = comment
        rating_obj[0].heading_for_comment = subject
        rating_obj[0].save()

        # calculate overall rating and save it
        calculate_overall_rating(page_type, search_by)

        # sent notification to Author
        try:
           sent_notictaion_email_to_author(page_type,search_by,name,star_value,page_title)
        except Exception as error:
           print("heyyyyyyyyyyyyyyyyyyyy=======>",error)

        return Response(RATING_SAVED.format(page_title.title()), status=status.HTTP_200_OK)

    except Exception as error:
        print("error---------------",error)
        return Response(OTP_ISSUE, status=status.HTTP_404_NOT_FOUND)

# @background(schedule=60)
# def sent_notictaion_email_to_author(page_type,search_by,name,star_value,page_title):
#     print("yessssssssssssssssssssssssssssssssss")
#     if page_type=="story":
#         obj = UserStoryTitle.objects.get(search_by=search_by)
#     elif page_type=="poem":
#         obj = UserPoem.objects.get(search_by=search_by)

#     notification_status = obj.notification
#     if notification_status=="ON":
#         page_title = page_title.title()
#         name = name.title()
#         first_name = (name.split()[0]).title()
#         author_email = obj.author.email
#         author_name = UserSignup.objects.get(email=author_email).full_name.split()[0]    
#         author_url = UrlPostfixHistory.objects.get(user_email=author_email).url_postfix

#         html_content = render_to_string('mail_template.html', {'var_name': author_name.title(), 'body_content':NOTIFICATION_EMAIL.format(name,page_type,page_title,first_name,star_value), 'terms_conditions':REVIEWER_LINK.format(author_url,page_type,search_by)})
#         send_email(NOTIFICATION_SUBJECT.format(page_title,name), html_content, [author_email])


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

     if page_type_obj.total_reviewer==0:
        page_type_obj.publish_date = timezone.now()

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


@api_view(['GET'])
def reviewers_detail(request):
    try:
        search_by = request.GET.get('search_by')
        #requested_page_no = request.GET.get('page',1)
        rating_queryset = Rating.objects.filter(rated_title=search_by)
        #page_obj = Paginator(rating_queryset, 6)
        #requested_page = page_obj.page(requested_page_no)

        reviewer_list = []
        for obj in rating_queryset:
            reviewer_dict = {}
            user_photo=""
            name = obj.user_name
            try:
               user_obj = UserSignup.objects.get(email=obj.rate_by)
               if user_obj.user_photo:
                  user_photo = HOST_NAME+"/media/"+str(user_obj.user_photo)
               name = user_obj.full_name
            except Exception as e:
               pass

            reviewer_dict["reviewer_photo"]=user_photo
            reviewer_dict["reviewer_name"]=name
            reviewer_dict["given_star"]=obj.rating_value
            reviewer_dict["date"]=obj.created_at

            # Check comment status
            comment = obj.comment
            subject=None
            if obj.block_this_comment:
               comment = ""
            else:
                if obj.heading_for_comment:
                   subject = (obj.heading_for_comment).title()

            reviewer_dict["comment"]=comment
            reviewer_dict["reviewer_subject"]= subject
            reviewer_list.append(reviewer_dict)
        return Response({"data":reviewer_list},status=status.HTTP_200_OK)

    except Exception as error:
        print("Errorrrrr",error)
        return Response(NOT_VALIDATE, status=status.HTTP_404_NOT_FOUND)



################# Finding Best writers #######################

@api_view(['GET'])
def top_writers_list(request):

    filter_by = request.GET.get('filter_by','both')
    if filter_by=='top_poets':
       poets_sublist = find_top_writers()[1]
       if poets_sublist:
          data = []
          for obj in poets_sublist:
              user_obj = UserSignup.objects.get(email=obj[0])
              user_photo = ""
              if user_obj.user_photo:
                  user_photo = HOST_NAME+"/media/"+str(user_obj.user_photo)
              data.append({"name":user_obj.full_name,"user_photo":user_photo})

          return Response(data,status=status.HTTP_200_OK)
       else:
          return Response(POETS, status=status.HTTP_404_NOT_FOUND)

    elif filter_by=='top_story_writer':
       story_writer_sublist = find_top_writers()[0]
       if story_writer_sublist:
          data = []
          for obj in story_writer_sublist:
              user_obj = UserSignup.objects.get(email=obj[0])
              user_photo = ""
              if user_obj.user_photo:
                  user_photo = HOST_NAME+"/media/"+str(user_obj.user_photo)
              data.append({"name":user_obj.full_name,"user_photo":user_photo})

          return Response(data,status=status.HTTP_200_OK)
       else:
          return Response(STORY_WRITERS, status=status.HTTP_404_NOT_FOUND)


    elif filter_by=='both':
       both_sublist = find_top_writers()[2]
       if both_sublist:
          data = []
          for obj in both_sublist:
              user_obj = UserSignup.objects.get(email=obj[0])
              user_photo = ""
              if user_obj.user_photo:
                  user_photo = HOST_NAME+"/media/"+str(user_obj.user_photo)
              data.append({"name":user_obj.full_name,"user_photo":user_photo})

          return Response(data,status=status.HTTP_200_OK)
       else:
          return Response(NO_WRITERS, status=status.HTTP_404_NOT_FOUND)

########## Logic to find top users ###################################

def find_top_writers():
    all_writers = UserSignup.objects.filter(status=True).values_list('email',flat=True)
    stroy_calculation = []
    poem_calculation = []
    both_calculation = []
    for author_email in all_writers:
        total_story = UserStoryTitle.objects.filter(author__email=author_email,privacy='PUBLIC',verified_content=True,total_reviewer__gte=1).values_list('overall_rating','total_reviewer')
        total_poems = UserPoem.objects.filter(author__email=author_email,privacy='PUBLIC',verified_content=True,total_reviewer__gte=1).values_list('overall_rating','total_reviewer')

        story_total_rating = 0
        story_total_reviewer = 0
        poem_total_rating = 0
        poem_total_reviewer = 0

        if total_story:
           for rating_review in total_story:
               story_total_rating = story_total_rating + rating_review[0]
               story_total_reviewer = story_total_reviewer + rating_review[1]

           avg_rating_per_book = story_total_rating/len(total_story)
           story_total_point = avg_rating_per_book*story_total_reviewer
           stroy_calculation.append([author_email,story_total_point])

        if total_poems:
           for rating_review in total_poems:
               poem_total_rating = poem_total_rating + rating_review[0]
               poem_total_reviewer = poem_total_reviewer + rating_review[1]

           avg_rating_per_poem = poem_total_rating/len(total_poems)
           poem_total_point = avg_rating_per_poem*poem_total_reviewer
           poem_calculation.append([author_email,poem_total_point])

        if total_story or total_poems:
           both_rating = story_total_rating+poem_total_rating
           total_story_poem = len(total_story)+len(total_poems)

           avg_rating_for_both = both_rating/total_story_poem
           total_reviewer_for_both = story_total_reviewer+poem_total_reviewer
           both_total_point = avg_rating_for_both*total_reviewer_for_both
           both_calculation.append([author_email,both_total_point])

    stroy_calculation = arrange_best_writers_order(stroy_calculation)
    poem_calculation = arrange_best_writers_order(poem_calculation)
    both_calculation = arrange_best_writers_order(both_calculation)

    return stroy_calculation,poem_calculation,both_calculation


def arrange_best_writers_order(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] < sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li


############### Poem and Story of the Week ######################################

@api_view(['GET'])
def poem_story_of_the_week(request):

    poem_queryset = UserPoem.objects.filter(total_reviewer__gte=1,verified_content=True,privacy='PUBLIC').order_by('-publish_date')
    poem_data = create_response_queryset(poem_queryset)
    story_queryset = UserStoryTitle.objects.filter(total_reviewer__gte=1,verified_content=True,privacy='PUBLIC').order_by('-publish_date')
    story_data = create_response_queryset(story_queryset)
    return Response({"story_data":story_data,"poem_data":poem_data,"poem_heading":POEM_HEADING,"poem_subject":POEM_SUBJECT,"poem_subject_by":POEM_SUBJECT_BY,"story_heading":STORY_HEADING,"story_subject":STORY_SUBJECT,"story_subject_by":STORY_SUBJECT_BY},status=status.HTTP_200_OK)

def create_response_queryset(queryset_obj):
    data = []
    for obj in queryset_obj:
        cover_photo = HOST_NAME+"/media/"+str(obj.default_image)
        auther_name = UserSignup.objects.get(email=obj.author.email).full_name
        author_url = UrlPostfixHistory.objects.get(user_email=obj.author.email).url_postfix
        data.append({"title":obj.title,"search_by":obj.search_by,"cover_photo":cover_photo,"publish_date":obj.publish_date,"author_name":auther_name,"overall_rating":obj.overall_rating,"post_fix":author_url,"title_choice":obj.title_choice})
    return data
