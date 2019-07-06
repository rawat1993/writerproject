from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.models import User
from .constants import *
from .views import send_email
from datetime import datetime
from django.template.loader import render_to_string
from django.db.models import Q
import uuid


# Register your models here.


# Settings for Super-admin

class UrlPostfixHistoryadmin(admin.ModelAdmin):
    list_display = ('user_email','url_postfix','status','action_taken_by','updated_at')
    readonly_fields = ['user_email','url_postfix','action_taken_by']
    search_fields = ('user_email','url_postfix')
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def save_model(self, request, obj, form, change):
           obj.action_taken_by = request.user
           obj.updated_at = datetime.now()
           obj.save()
           user_obj = UserSignup.objects.get(email=obj.user_email)
           user_name = user_obj.full_name.split()[0]
           if obj.status=='BLOCK':
              super_user_obj = User.objects.get(username=obj.user_email)
              super_user_obj.is_active = False
              super_user_obj.save()
              user_obj.status = False
              user_obj.save()
              html_content = render_to_string('mail_template.html', {'var_name': user_name.title(), 'body_content':POSTFIX_BLOCKED_EMAIL, 'terms_conditions':WC_TERMS_AND_CONDTIONS})
              send_email(SUBJECT_FOR_POSTFIX_BLOCKED_EMAIL, html_content, [obj.user_email])

           elif obj.status=='UNBLOCK':
              super_user_obj = User.objects.get(username=obj.user_email)
              super_user_obj.is_active = True
              super_user_obj.save()
              user_obj.status = True
              user_obj.save()
              html_content = render_to_string('mail_template.html', {'var_name': user_name.title(), 'body_content':POSTFIX_REACTIVATE_EMAIL})
              send_email(SUBJECT_FOR_REACTIVATE_POSTFIX, html_content, [obj.user_email])


class AboutUsAdmin(SummernoteModelAdmin):
    summernote_fields = 'content'
    readonly_fields = ["about_us"]

    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False

admin.site.site_url = None
admin.site.register(UrlPostfixHistory,UrlPostfixHistoryadmin)
admin.site.register(LoggingHistory)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(EmailOTP)

# Settings for User-admin
# User independent admin sites
class UserAdminSite(AdminSite):
    site_header = "User Admin Site"
    site_title = "User Admin Portal"
    index_title = "Welcome to writer admin Portal"


class UserBlogAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = 'content'
    list_display = ('blog_part','title')

    #def save_model(self, request, obj, form, change):
    #       obj.blog_part="".join((obj.blog_part).split())
    #       obj.save()

    def get_queryset(self, request):
        qs = super(UserBlogAdmin, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(title__author=request.user)


    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['title'].queryset = UserBlogTitle.objects.filter(author=request.user)
         return super(UserBlogAdmin, self).render_change_form(request, context, *args, **kwargs)


class UserStoryAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = 'content'
    list_display = ('story_seen_no','title')

    def has_change_permission(self, request, obj=None):
      if not obj.__str__() =='None':     
        if UserStory.objects.filter(Q(title__title=obj.__str__()) & Q(title__author=request.user) & Q(title__published_content='YES')):
          return False
        else:
          return True

    def has_delete_permission(self, request, obj=None):
      if not obj.__str__() =='None':     
        if UserStory.objects.filter(Q(title__title=obj.__str__()) & Q(title__author=request.user) & Q(title__published_content='YES')):
          return False
        else:
          return True

    def get_queryset(self, request):
        qs = super(UserStoryAdmin, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(title__author=request.user)


    def render_change_form(self, request, context, *args, **kwargs):
        if kwargs['obj']==None or not UserStory.objects.filter(Q(title__title=kwargs['obj'].title.title) & Q(title__author=request.user) & Q(title__published_content='YES')):
          context['adminform'].form.fields['title'].queryset = UserStoryTitle.objects.filter(author=request.user, published_content='NO')
          return super(UserStoryAdmin, self).render_change_form(request, context, *args, **kwargs)     
        else:
           # context['adminform'].form.fields['title'].queryset = UserStory.objects.filter(title__author=request.user)
           return super(UserStoryAdmin, self).render_change_form(request, context, *args, **kwargs) 


class UserPoemAdmin(SummernoteModelAdmin):
    summernote_fields = 'content'
    list_display = ('title','search_by','published_content','view_on_website')
    # readonly_fields = ["published_content"]

    def has_change_permission(self, request, obj=None):
      if UserPoem.objects.filter(Q(title=obj.__str__()) & Q(author=request.user) & Q(published_content='YES')):
        return False
      else:
        return True

    def has_delete_permission(self, request, obj=None):
      if UserPoem.objects.filter(Q(title=obj.__str__()) & Q(author=request.user) & Q(published_content='YES')):
        return False
      else:
        return True

    def save_model(self, request, obj, form, change):
           obj.author = request.user
           obj.coming_soon = "Coming Soon"
           obj.save()
           all_data = UserPoem.objects.filter(author=obj.author)
           if not obj.search_by:
              obj.search_by = genrate_random(all_data,obj.title)
              obj.save()

           # Generate view link for the user

           if obj.published_content=='YES':
              obj.view_on_website = ""
              obj.coming_soon = ""
              obj.save()
           else:   
              url_postfix = UrlPostfixHistory.objects.get(user_email=request.user.email).url_postfix
              key = uuid.uuid4()
              generate_link = VIEW_LINK.format(url_postfix,'poem',key)
              UserPoem.objects.filter(published_content='NO',author=request.user).update(view_on_website=generate_link)

              # create or updating the key
              admin_key_obj = AdminKeys.objects.get_or_create(url_postfix=url_postfix,key_for='poem')
              admin_key_obj[0].key = key
              admin_key_obj[0].save()

           # Enter data in ContentVerified Table
           try:
              ContentVerified.objects.get(title=obj.search_by)
           except:
              ContentVerified.objects.create(action_for='poem',title=obj.search_by)


    def get_queryset(self, request):
        qs = super(UserPoemAdmin, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(author=request.user)


user_admin_site = UserAdminSite(name='user_admin')

# Remove View Site link from django-admin Panel
user_admin_site.site_url = None

user_admin_site.register(UserBlog,UserBlogAdmin)
user_admin_site.register(UserStory,UserStoryAdmin)
user_admin_site.register(UserPoem,UserPoemAdmin)


class UserProfile(admin.ModelAdmin):
    list_display = ('full_name','phone_number','city','state')
    readonly_fields = ["email"]
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def get_queryset(self, request):
        qs = super(UserProfile, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(email=request.user.username)

user_admin_site.register(UserSignup,UserProfile)



# User Blog Title

class UserBlogTitleAdmin(SummernoteModelAdmin):
    list_display = ('title','search_by','published_content','view_on_website')
    def save_model(self, request, obj, form, change):
           obj.author = request.user
           obj.save()
           all_data = UserBlogTitle.objects.filter(author=obj.author)
           if not obj.search_by:
              obj.search_by = genrate_random(all_data,obj.title)
              obj.save()

           # Generate view link for the user
           url_postfix = UrlPostfixHistory.objects.get(user_email=request.user.email).url_postfix
           key = uuid.uuid4()
           generate_link = VIEW_LINK.format(url_postfix,'story',key)
           obj.view_on_website = generate_link
           obj.save()

           # create or updating the key
           admin_key_obj = AdminKeys.objects.get_or_create(url_postfix=url_postfix,key_for=obj.search_by)
           admin_key_obj[0].key = key
           admin_key_obj[0].save()

           # Enter data in ContentVerified Table
           try:
              ContentVerified.objects.get(title=obj.search_by)
           except:
              ContentVerified.objects.create(action_for='blog',title=obj.search_by)

    def get_queryset(self, request):
        qs = super(UserBlogTitleAdmin, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(author=request.user)

user_admin_site.register(UserBlogTitle,UserBlogTitleAdmin)


class UserStroyTitleAdmin(SummernoteModelAdmin):
    list_display = ('title','search_by','published_content','view_on_website')


    def has_change_permission(self, request, obj=None):
      if UserStoryTitle.objects.filter(Q(title=obj.__str__()) & Q(author=request.user) & Q(published_content='YES')):
        return False
      else:
        return True

    def has_delete_permission(self, request, obj=None):
      if UserStoryTitle.objects.filter(Q(title=obj.__str__()) & Q(author=request.user) & Q(published_content='YES')):
        return False
      else:
        return True


    def save_model(self, request, obj, form, change):
           obj.author = request.user
           obj.coming_soon = "Coming Soon"
           obj.save()
           all_data = UserStoryTitle.objects.filter(author=obj.author)
           if not obj.search_by:
              obj.search_by = genrate_random(all_data,obj.title)
              obj.save()

           # Generate view link for the user
           if obj.published_content=='YES':
              obj.view_on_website = ""
              obj.coming_soon = ""
              obj.save()
           else:   
              url_postfix = UrlPostfixHistory.objects.get(user_email=request.user.email).url_postfix
              key = uuid.uuid4()
              generate_link = VIEW_LINK.format(url_postfix,'story',key)
              UserStoryTitle.objects.filter(published_content='NO',author=request.user).update(view_on_website=generate_link)

              # create or updating the key
              admin_key_obj = AdminKeys.objects.get_or_create(url_postfix=url_postfix,key_for='story')
              admin_key_obj[0].key = key
              admin_key_obj[0].save()

           # Enter data in ContentVerified Table
           try:
              ContentVerified.objects.get(title=obj.search_by)
           except:
              ContentVerified.objects.create(action_for='story',title=obj.search_by)

    def get_queryset(self, request):
        qs = super(UserStroyTitleAdmin, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(author=request.user)

user_admin_site.register(UserStoryTitle,UserStroyTitleAdmin)



# Generate random string for search_by

def genrate_random(previous_serarch_by,title):
           list_search_by = list(previous_serarch_by.values_list('search_by',flat=True))
           split_title = title.split(' ')
           # Removed null values from list
           split_title = list(filter(None, split_title))
           search_by = ""
           flag = 0
           death = 2
           for word in range(0,len(split_title)):
              if len(search_by)<=20:
                 old = search_by
                 if split_title[word]:
                    search_by = search_by+split_title[word]
                 if len(search_by)>20:
                    death = word
                    flag = 1

           if flag==1:
              search_by = old
           search_by = search_by.lower()
           if search_by in list_search_by:
              removed_last_word = search_by[:-len(split_title[death-1])]
              add_this = split_title[(len(split_title))-1]
              search_by = removed_last_word+add_this
              search_by = search_by.lower()
              if search_by in list_search_by:
                 import random, string
                 letters = string.ascii_lowercase
                 random_string = ''.join(random.choice(letters) for i in range(4))
                 search_by = removed_last_word+random_string

           return search_by.lower()


######################## Reviewers Listing ###################

class RatingAdmin(admin.ModelAdmin):
    list_display = ('rate_by','rating_value','rated_title')
    readonly_fields = ['rate_by','user_name','rating_value','rated_title','heading_for_comment','comment']
    search_fields = ('rate_by','rated_title')
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Rating,RatingAdmin)


######################### Fake Raters blocking ################

class FakeRatersAdmin(admin.ModelAdmin):
    list_display = ('email','status','action_taken_by')
    readonly_fields = ['action_taken_by']
    search_fields = ('email',)
    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
           obj.action_taken_by = request.user
           obj.save()

admin.site.register(FakeRaters,FakeRatersAdmin)
admin.site.register(AdminKeys)

######################## Verified content logic ########################

class ContentVerifiedAdmin(admin.ModelAdmin):
    list_display = ('title','resion','action_taken_by','updated_at','created_at')
    readonly_fields = ['action_for','title','action_taken_by']
    search_fields = ('title',)
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
           obj.action_taken_by = request.user
           obj.updated_at = datetime.now()
           obj.save()
           email, username, title_name, title_obj = retun_user_email(obj)
           if obj.resion=='COPYRIGHT':
                 body_content = COPYRIGHT_EMAIL.format(title_name,(obj.action_for).title())
                 title_obj.verified_content = False
                 title_obj.save()
           elif obj.resion=='SEXUAL':
                 body_content = SEXUAL_CONTENT_EMAIL.format(title_name,(obj.action_for).title())
                 title_obj.verified_content = False
                 title_obj.save()
           elif obj.resion=='ACTIVE':
                 body_content = ACTIVE_CONTENT_EMAIL.format(title_name,(obj.action_for).title())
                 title_obj.verified_content = True
                 title_obj.save()

           html_content = render_to_string('mail_template.html', {'var_name': username.title(), 'body_content':body_content,'terms_conditions':WC_TERMS_AND_CONDTIONS})
           send_email(SUBJECT_FOR_VERIFY_CONTENT, html_content, [email])


def retun_user_email(obj):
    if obj.action_for=='story':
       title_obj = UserStoryTitle.objects.get(search_by=obj.title)
    elif obj.action_for=='poem':
       title_obj = UserPoem.objects.get(search_by=obj.title)
    elif obj.action_for=='blog':
       title_obj = UserBlogTitle.objects.get(search_by=obj.title)

    title_name = title_obj.title
    user_email = title_obj.author.email
    user_name = UserSignup.objects.get(email=user_email).full_name.split()[0]

    return user_email,user_name,title_name,title_obj

admin.site.register(ContentVerified,ContentVerifiedAdmin)
