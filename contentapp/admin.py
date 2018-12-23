from django.contrib import admin
from django.contrib.admin import AdminSite
from contentapp.models import *
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

admin.site.register(LoggingHistory)

# User independent admin sites
class UserAdminSite(AdminSite):
    site_header = "User Admin Site"
    site_title = "User Admin Portal"
    index_title = "Welcome to User admin Portal"


class UserContentAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
        summernote_fields = 'content'
        list_display = ('title','short_description','content','privacy','status')

user_admin_site = UserAdminSite(name='user_admin')
user_admin_site.register(UserSignup)
user_admin_site.register(UserBlog,UserContentAdmin)
user_admin_site.register(UserStory,UserContentAdmin)
user_admin_site.register(UserPoem,UserContentAdmin)






















