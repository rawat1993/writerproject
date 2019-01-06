from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.models import User
# Register your models here.


# Settings for Super-admin

class UrlPostfixHistoryadmin(admin.ModelAdmin):
    list_display = ('user_email','url_postfix','status','action_taken_by')
    readonly_fields = ['user_email','url_postfix','action_taken_by']
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def save_model(self, request, obj, form, change):
           obj.action_taken_by = request.user
           obj.save()
           if obj.status=='BLOCK':
              super_user_obj = User.objects.get(username=obj.user_email)
              super_user_obj.is_active = False
              super_user_obj.save()
           elif obj.status=='UNBLOCK':
              super_user_obj = User.objects.get(username=obj.user_email)
              super_user_obj.is_active = True
              super_user_obj.save()

admin.site.register(UrlPostfixHistory,UrlPostfixHistoryadmin)
admin.site.register(LoggingHistory)

# Settings for User-admin
# User independent admin sites
class UserAdminSite(AdminSite):
    site_header = "User Admin Site"
    site_title = "User Admin Portal"
    index_title = "Welcome to User admin Portal"


class UserBlogAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = 'content'
    list_display = ('blog_part','title','total_hits')
    readonly_fields = ["total_hits"]
    def save_model(self, request, obj, form, change):
           obj.blog_part="".join((obj.blog_part).split())
           obj.save()

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
    list_display = ('story_seen_no','title','total_hits') 
    readonly_fields = ["total_hits"]
    def save_model(self, request, obj, form, change):
        obj.story_seen_no="".join((obj.story_seen_no).split())
        obj.save()
    def get_queryset(self, request):
        qs = super(UserStoryAdmin, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(title__author=request.user)


    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['title'].queryset = UserStoryTitle.objects.filter(author=request.user)
         return super(UserStoryAdmin, self).render_change_form(request, context, *args, **kwargs)



class UserPoemAdmin(SummernoteModelAdmin):
    summernote_fields = 'content'
    list_display = ('title','short_description','privacy','total_hits','search_by')
    readonly_fields = ["total_hits"]
    def save_model(self, request, obj, form, change):
           obj.author = request.user
           obj.save()
           all_data = UserPoem.objects.filter(author=obj.author)
           if not obj.search_by:
              obj.search_by = genrate_random(all_data,obj.title)
              obj.save()
    def get_queryset(self, request):
        qs = super(UserPoemAdmin, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(author=request.user)


user_admin_site = UserAdminSite(name='user_admin')
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
    readonly_fields = ["total_hits"]
    list_display = ('title','short_description','privacy','search_by','total_hits')
    def save_model(self, request, obj, form, change):
           obj.author = request.user
           obj.save()
           all_data = UserBlogTitle.objects.filter(author=obj.author)
           if not obj.search_by:
              obj.search_by = genrate_random(all_data,obj.title)
              obj.save()
    def get_queryset(self, request):
        qs = super(UserBlogTitleAdmin, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(author=request.user)

user_admin_site.register(UserBlogTitle,UserBlogTitleAdmin)


class UserStroyTitleAdmin(SummernoteModelAdmin):
    readonly_fields = ["total_hits"]
    list_display = ('title','short_description','privacy','total_hits','search_by')
    def save_model(self, request, obj, form, change):
           obj.author = request.user
           obj.save()
           all_data = UserStoryTitle.objects.filter(author=obj.author)
           if not obj.search_by:
              obj.search_by = genrate_random(all_data,obj.title)
              obj.save()            
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
