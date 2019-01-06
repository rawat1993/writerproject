# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from contentapp.models import UrlPostfixHistory,UserSignup,UserStoryTitle,UserBlogTitle,UserPoem,UserStory,UserBlog
from contentapp.serializers import UserSignup_Serializer,UserStoryTitleSerializer,UserBlogTitleSerializer,UserPoemSerializer,UserStorySerializer,UserPoemContentSerializer,UserBlogSerializer
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
            if subject==STORY:
               story_list = UserStoryTitle.objects.filter(Q(author__username=user_email) & Q(privacy='PUBLIC'))
               if not story_list:
                  return Response(NOT_AVAILABLE.format(STORY),status=status.HTTP_404_NOT_FOUND)               
               serializer = UserStoryTitleSerializer(story_list, many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)

            elif subject==BLOG:
               blog_list = UserBlogTitle.objects.filter(Q(author__username=user_email) & Q(privacy='PUBLIC'))
               if not blog_list:
                  return Response(NOT_AVAILABLE.format(BLOG),status=status.HTTP_404_NOT_FOUND)                
               serializer = UserBlogTitleSerializer(blog_list, many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)

            elif subject==POEM:
               poem_list = UserPoem.objects.filter(Q(author__username=user_email) & Q(privacy='PUBLIC'))
               if not poem_list:
                  return Response(NOT_AVAILABLE.format(POEM),status=status.HTTP_404_NOT_FOUND)               
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
               user_stroy_detail = UserStory.objects.filter(Q(title__author__username=user_email) & (Q(title__search_by=title) & Q(title__privacy='PUBLIC')))
               if not user_stroy_detail:
                  return Response(TITLE_NOT_FOUND.format(title),status=status.HTTP_404_NOT_FOUND)               
               serializer = UserStorySerializer(user_stroy_detail, many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)

            elif subject==BLOG:
               blog_content = UserBlog.objects.filter(Q(title__author__username=user_email) & (Q(title__search_by=title) & Q(title__privacy='PUBLIC')))
               if not blog_content:
                  return Response(TITLE_NOT_FOUND.format(title),status=status.HTTP_404_NOT_FOUND)               
               serializer = UserBlogSerializer(blog_content, many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)

            elif subject==POEM:
               poem_content = UserPoem.objects.filter(Q(author__username=user_email) & (Q(search_by=title) & Q(privacy='PUBLIC')))
               if not poem_content:
                  return Response(TITLE_NOT_FOUND.format(title),status=status.HTTP_404_NOT_FOUND)               
               serializer = UserPoemContentSerializer(poem_content, many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)       

            return Response(URL_NOT_CORRECT,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("Errrror==>",error)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PageForTitleView(APIView):

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
            page = kwargs['page']
            if subject==STORY:
               user_stroy_detail = UserStory.objects.filter(Q(title__author__username=user_email) & (Q(title__search_by=title) & Q(title__privacy='PUBLIC')))
               if user_stroy_detail:
                  page_obj = user_stroy_detail.get(story_seen_no=page)
               else:
                return Response(TITLE_NOT_FOUND.format(title),status=status.HTTP_404_NOT_FOUND)
                  
               serializer = UserStorySerializer(page_obj)
               return Response(serializer.data,status=status.HTTP_200_OK)

            # elif subject==BLOG:
            #    blog_content = UserBlog.objects.filter(Q(title__author__username=user_email) & (Q(title__search_by=title) & Q(title__privacy='PUBLIC')))
            #    serializer = UserBlogSerializer(blog_content, many=True)
            #    return Response(serializer.data,status=status.HTTP_200_OK)

            # elif subject==POEM:
            #    poem_content = UserPoem.objects.filter(Q(author__username=user_email) & (Q(search_by=title) & Q(privacy='PUBLIC')))
            #    serializer = UserPoemContentSerializer(poem_content, many=True)
            #    return Response(serializer.data,status=status.HTTP_200_OK)        

            return Response(URL_NOT_CORRECT,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("Errrror==>",error)
            return Response(PAGE_NOT_FOUND.format(page),status=status.HTTP_404_NOT_FOUND)