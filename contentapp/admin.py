from django.contrib import admin
from contentapp.models import WriterProfile
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class WriterProfileAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
        summernote_fields = 'template_render'
        list_display = ('first_name','last_name','email','phone_number')

admin.site.register(WriterProfile, WriterProfileAdmin)
