# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from contentapp.models import UrlPostfixHistory,UserSignup,UserStoryTitle,UserBlogTitle,UserPoem,UserStory,UserBlog,AdminKeys,UserQuotes
from contentapp.serializers import UserSignup_Serializer,UserStoryTitleSerializer,UserBlogTitleSerializer,UserPoemSerializer,UserStorySerializer,UserPoemContentSerializer,UserBlogSerializer
from .constants import *
from django.db.models import Q
from django.core.paginator import Paginator
import re

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
            story_status = "no"
            blog_status = "no"
            poem_status = "no"
            quotes_status = "no"
            story_list = UserStoryTitle.objects.filter(Q(author__username=user_email) & Q(published_content='YES'))
            if story_list:
               story_status = "yes"
            blog_list = UserBlogTitle.objects.filter(Q(author__username=user_email) & Q(published_content='YES'))
            if blog_list:
               blog_status = "yes"
            poem_list = UserPoem.objects.filter(Q(author__username=user_email) & Q(published_content='YES'))
            if poem_list:
               poem_status = "yes"
            quotes_list = UserQuotes.objects.filter(Q(author__username=user_email) & Q(published_content='YES'))
            if quotes_list:
               quotes_status = "yes"

            return Response({"data":serializer.data,"story_status":story_status,"blog_status":blog_status,"poem_status":poem_status,"quotes_status":quotes_status},status=status.HTTP_200_OK)
        except Exception as error:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectView(APIView):

    def get(self,request,**kwargs):
        try:
            post_fix = kwargs['post_fix_value']
            requested_page_no = request.GET.get('page',1)
            admin_key = request.GET.get('key',False)                           
            user_email = user_status(post_fix)
            if user_email == "NOT_FOUND":
                return Response(USER_POSTFIX_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            elif user_email == "USER_BLOCKED":
                 return Response(POSTFIX_STATUS,status=status.HTTP_401_UNAUTHORIZED)
            subject = kwargs['subject']

            by_admin="YES"
            if admin_key:
               try:
                  AdminKeys.objects.get(key=admin_key,url_postfix=post_fix,key_for=subject)
                  by_admin="NO"
               except Exception as e:
                  pass

            if subject==STORY:
               story_list = UserStoryTitle.objects.filter(Q(author__username=user_email) & Q(verified_content=True) & Q(published_content=by_admin)).order_by('-created_at')
               if not story_list:
                  return Response(NOT_AVAILABLE.format(STORY),status=status.HTTP_404_NOT_FOUND)
               page_obj = Paginator(story_list, 6)
               requested_page = page_obj.page(requested_page_no)
               serializer = UserStoryTitleSerializer(requested_page, many=True)
               return Response({"data":serializer.data,"total_pages":page_obj.num_pages},status=status.HTTP_200_OK)

            elif subject==BLOG:
               blog_list = UserBlogTitle.objects.filter(Q(author__username=user_email) & Q(verified_content=True) & Q(published_content=by_admin)).order_by('-created_at')
               if not blog_list:
                  return Response(NOT_AVAILABLE.format(BLOG),status=status.HTTP_404_NOT_FOUND)
               page_obj = Paginator(blog_list, 6)
               requested_page = page_obj.page(requested_page_no)
               serializer = UserBlogTitleSerializer(requested_page, many=True)
               return Response({"data":serializer.data,"total_pages":page_obj.num_pages},status=status.HTTP_200_OK)

            elif subject==POEM:
               poem_list = UserPoem.objects.filter(Q(author__username=user_email) & Q(verified_content=True) & Q(published_content=by_admin)).order_by('-created_at')
               if not poem_list:
                  return Response(NOT_AVAILABLE.format(POEM),status=status.HTTP_404_NOT_FOUND)
               page_obj = Paginator(poem_list, 6)
               requested_page = page_obj.page(requested_page_no)
               serializer = UserPoemSerializer(requested_page, many=True)
               return Response({"data":serializer.data,"total_pages":page_obj.num_pages},status=status.HTTP_200_OK)

            elif subject==QUOTES:
               quotes_list = UserQuotes.objects.filter(Q(author__username=user_email) & Q(verified_content=True) & Q(published_content=by_admin)).order_by('-created_at')
               if not quotes_list:
                  return Response(QUOTES_NOT_AVAILABLE,status=status.HTTP_404_NOT_FOUND)
   
               page_obj = Paginator(quotes_list, 6)
               requested_page = page_obj.page(requested_page_no)
               
               data=[]
               for quote_obj in requested_page:
                   quote_image = DEFAULT_IMAGE_PATH
                   text_color = quote_obj.text_color

                   if quote_obj.quote_image:
                      quote_image = HOST_NAME+"/media/"+str(quote_obj.quote_image)               

                   data.append({"quote_id":quote_obj.quote_id,"quote_text":quote_obj.content,"quote_image":quote_image,"text_color":text_color,"coming_soon":quote_obj.coming_soon,"updated_at":quote_obj.updated_at})
               return Response({"data":data,"total_pages":page_obj.num_pages},status=status.HTTP_200_OK)


            return Response(URL_NOT_CORRECT,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("------------------>",error)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TitleView(APIView):

    def get(self,request,**kwargs):
        try:
            post_fix = kwargs['post_fix_value']
            admin_key = request.GET.get('key',False)
            user_email = user_status(post_fix)
            if user_email == "NOT_FOUND":
                return Response(USER_POSTFIX_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            elif user_email == "USER_BLOCKED":
                 return Response(POSTFIX_STATUS,status=status.HTTP_401_UNAUTHORIZED)

            by_admin="YES"
            subject = kwargs['subject']
            if admin_key:
               try:
                  AdminKeys.objects.get(key=admin_key,url_postfix=post_fix,key_for=subject)
                  by_admin="NO"
               except Exception as e:
                  pass

            title = kwargs['title']
            if subject==STORY:
               user_stroy_detail = UserStory.objects.filter(Q(title__author__username=user_email) & (Q(title__search_by=title) & Q(title__verified_content=True) & Q(title__published_content=by_admin))).order_by('created_at')
               if not user_stroy_detail:
                  return Response(TITLE_NOT_FOUND.format("Story"),status=status.HTTP_404_NOT_FOUND)
               seen_list = user_stroy_detail.values_list('story_seen_no',flat=True)
               #serializer = UserStorySerializer(user_stroy_detail, many=True)
               data = append_baseUrl(user_stroy_detail,"story")
               return Response({"data":data,"seen_list":seen_list},status=status.HTTP_200_OK)

            elif subject==BLOG:
               blog_content = UserBlog.objects.filter(Q(title__author__username=user_email) & (Q(title__search_by=title) & Q(title__verified_content=True) & Q(title__published_content=by_admin))).order_by('created_at')
               if not blog_content:
                  return Response(TITLE_NOT_FOUND.format("Blog"),status=status.HTTP_404_NOT_FOUND)
               blog_part_list = blog_content.values_list('blog_part',flat=True)
               #serializer = UserBlogSerializer(blog_content, many=True)
               data = append_baseUrl(blog_content,"blog")
               return Response({"data":data,"seen_list":blog_part_list},status=status.HTTP_200_OK)

            elif subject==POEM:
               poem_content = UserPoem.objects.filter(Q(author__username=user_email) & (Q(search_by=title) & Q(verified_content=True) & Q(published_content=by_admin)))
               if not poem_content:
                  return Response(TITLE_NOT_FOUND.format("Poem"),status=status.HTTP_404_NOT_FOUND)
               #serializer = UserPoemContentSerializer(poem_content, many=True)
               data = append_baseUrl(poem_content,"poem")
               return Response({"data":data},status=status.HTTP_200_OK)

            elif subject==QUOTES:
               quotes_list = UserQuotes.objects.filter(Q(author__username=user_email) & (Q(quote_id=str(title)) & Q(verified_content=True) & Q(published_content=by_admin)))
               if not quotes_list:
                  return Response(QUOTES_ID_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)

               data=[]
               for quote_obj in quotes_list:
                   quote_image = DEFAULT_IMAGE_PATH
                   text_color = quote_obj.text_color

                   if quote_obj.quote_image:
                      quote_image = HOST_NAME+"/media/"+str(quote_obj.quote_image)               
                   data.append({"quote_id":quote_obj.quote_id,"quote_text":quote_obj.content,"quote_image":quote_image,"text_color":text_color})

               return Response({"data":data},status=status.HTTP_200_OK)

            return Response(URL_NOT_CORRECT,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("Errrror==>",error)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def append_baseUrl(queryset_obj,object_type):
    updated_list = []
    for obj in queryset_obj:
        content_data = obj.content
        r = re.compile('(?<=src=").*?(?=")')
        src_list = r.findall(content_data)

        if src_list:
           for src in src_list:
               if src.startswith("/media"):
                  content_data = content_data.replace(
                                src, HOST_NAME + src)
        if object_type=="story":
           updated_list.append({"id":obj.id,"content":content_data,"story_seen_no":obj.story_seen_no})
        elif object_type=="blog":
           updated_list.append({"id":obj.id,"content":content_data,"blog_part":obj.blog_part})
        elif object_type=="poem":
           updated_list.append({"id":obj.id,"title":obj.title,"short_description":obj.short_description,"content":content_data})
        elif object_type=="about-us":
           updated_list.append({"content":content_data})         


    return updated_list


class PageForTitleView(APIView):

    def get(self,request,**kwargs):
        try:
            post_fix = kwargs['post_fix_value']
            user_email = user_status(post_fix)
            if user_email == "NOT_FOUND":
                return Response(USER_POSTFIX_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            elif user_email == "USER_BLOCKED":
                 return Response(POSTFIX_STATUS,status=status.HTTP_401_UNAUTHORIZED)

            subject = kwargs['subject']
            title = kwargs['title']
            page = kwargs['page']
            if subject==STORY:
               user_stroy_detail = UserStory.objects.filter(Q(title__author__username=user_email) & (Q(title__search_by=title) & Q(title__verified_content=True)))
               if user_stroy_detail:
                  page_obj = user_stroy_detail.get(story_seen_no=page)
               else:
                return Response(TITLE_NOT_FOUND.format(title),status=status.HTTP_404_NOT_FOUND)

               serializer = UserStorySerializer(page_obj)
               return Response(serializer.data,status=status.HTTP_200_OK)

            elif subject==BLOG:
                blog_content = UserBlog.objects.filter(Q(title__author__username=user_email) & (Q(title__search_by=title) & Q(title__verified_content=True)))
                if blog_content:
                   page_obj = blog_content.get(blog_part=page)
                else:
                   return Response(TITLE_NOT_FOUND.format(title),status=status.HTTP_404_NOT_FOUND)

                serializer = UserBlogSerializer(page_obj)
                return Response(serializer.data,status=status.HTTP_200_OK)

            # elif subject==POEM:
            #    poem_content = UserPoem.objects.filter(Q(author__username=user_email) & (Q(search_by=title) & Q(privacy='PUBLIC')))
            #    serializer = UserPoemContentSerializer(poem_content, many=True)
            #    return Response(serializer.data,status=status.HTTP_200_OK)

            return Response(URL_NOT_CORRECT,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("Errrror==>",error)
            return Response(PAGE_NOT_FOUND.format(page),status=status.HTTP_404_NOT_FOUND)


class TitleDetail(APIView):

    def get(self,request):
        search_by = request.GET.get('search_by')
        subject = request.GET.get('subject')
        url_postfix = request.GET.get('user')
        user_email = user_status(url_postfix)

        if user_email == "NOT_FOUND":
              return Response(USER_POSTFIX_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        elif user_email == "USER_BLOCKED":
              return Response(POSTFIX_STATUS,status=status.HTTP_401_UNAUTHORIZED)

        elif subject == "story":
           story_detail = UserStoryTitle.objects.get(search_by=search_by)
           serializer = UserStoryTitleSerializer(story_detail)
        elif subject == "blog":
           blog_detail = UserBlogTitle.objects.get(search_by=search_by)
           serializer = UserBlogTitleSerializer(blog_detail)
        elif subject == "poem":
           poem_detail = UserPoem.objects.get(search_by=search_by)
           serializer = UserPoemSerializer(poem_detail)

        return Response(serializer.data,status=status.HTTP_200_OK)

