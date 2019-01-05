# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from contentapp.models import UrlPostfixHistory,UserSignup,UserStoryTitle,UserBlogTitle,UserPoem,UserStory
from contentapp.serializers import UserSignup_Serializer,UserStoryTitleSerializer,UserBlogTitleSerializer,UserPoemSerializer,UserStorySerializer
from .constants import *
from django.db.models import Q


def user_status(post_fix_value):
    try:
       url_postfix_obj = UrlPostfixHistory.objects.get(url_postfix=post_fix_value)
       if url_postfix_obj.status == "BLOCK":
          return "USER_BLOCKED"
       user_email = url_postfix_obj.user_email 
       return user_email
    except Exception as error:
        return "NOT_FOUND"

class UserProfileView(APIView):

    def get(self,request,**kwargs):
        try:
            post_fix = kwargs['post_fix_value']
            user_email = user_status(post_fix)
            if user_email == "NOT_FOUND":
                return Response(USER_POSTFIX_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            elif user_email == "USER_BLOCKED":
                 return Response(POSTFIX_STATUS,status=status.HTTP_401_UNAUTHORIZED)

            user_obj = UserSignup.objects.get(email=user_email)
            serializer = UserSignup_Serializer(user_obj)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectView(APIView):

    def get(self,request,**kwargs):
        try:
            post_fix = kwargs['post_fix_value']
            user_email = user_status(post_fix)
            if user_email == "NOT_FOUND":
                return Response(USER_POSTFIX_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            elif user_email == "USER_BLOCKED":
                 return Response(POSTFIX_STATUS,status=status.HTTP_401_UNAUTHORIZED)
            
            subject = kwargs['subject']
            if post_fix==STORY:
               story_list = UserStoryTitle.objects.filter(Q(author__username=user_email) & Q(privacy='PUBLIC'))
               serializer = UserStoryTitleSerializer(story_list, many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)

            elif subject==BLOG:
               blog_list = UserBlogTitle.objects.filter(Q(author__username=user_email) & Q(privacy='PUBLIC'))
               serializer = UserBlogTitleSerializer(blog_list, many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)

            elif subject==POEM:
               poem_list = UserPoem.objects.filter(Q(author__username=user_email) & Q(privacy='PUBLIC'))
               serializer = UserPoemSerializer(poem_list, many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)              

            return Response(URL_NOT_CORRECT,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TitleView(APIView):

    def get(self,request,**kwargs):
        try:
            post_fix = kwargs['post_fix_value']
            print(kwargs,"000000000000")
            user_email = user_status(post_fix)
            if user_email == "NOT_FOUND":
                return Response(USER_POSTFIX_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            elif user_email == "USER_BLOCKED":
                 return Response(POSTFIX_STATUS,status=status.HTTP_401_UNAUTHORIZED)

            subject = kwargs['subject']
            title = kwargs['title']
            if subject==STORY:
               user_stroy_detail = UserStory.objects.filter(Q(title__author__username=user_email) & Q(title__search_by=title))
               serializer = UserStorySerializer(user_stroy_detail, many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)

            # elif post_fix==BLOG:
            #    blog_list = UserBlogTitle.objects.filter(Q(author__username=user_email) & Q(privacy='PUBLIC'))
            #    serializer = UserBlogTitleSerializer(blog_list, many=True)
            #    return Response(serializer.data,status=status.HTTP_200_OK)

            # elif post_fix==POEM:
            #    poem_list = UserPoem.objects.filter(Q(author__username=user_email) & Q(privacy='PUBLIC'))
            #    serializer = UserPoemSerializer(poem_list, many=True)
            #    return Response(serializer.data,status=status.HTTP_200_OK)              

            return Response(URL_NOT_CORRECT,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("Error========>",error)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class FifthUserProfileView(APIView):

    def get(self,request,**kwargs):
        try:
            print("------------",request.data,kwargs)
            # post_fix = request.GET['post_fix_value']
            # url_postfix_obj = UrlPostfixHistory.objects.get(url_postfix=post_fix)
            # user_email = url_postfix_obj.user_email
            # user_obj = UserSignup.objects.get(email=user_email,status=True)
            # serializer = UserSignup_Serializer(user_obj)
            return Response("444444444444444",status=status.HTTP_200_OK)
        except Exception as error:
            print("Error======>",error)
            return Response(USER_POSTFIX_NOT_FOUND,status=status.HTTP_400_BAD_REQUEST)