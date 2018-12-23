from django.forms import ModelForm
from django import forms
from contentapp.models import UserSignup
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

# class UserSignupForm(ModelForm):
#    class Meta:
#       model = UserSignup
#       fields = ['user_text']

class UserSignupForm(forms.Form):
   user_blog = forms.CharField(widget=SummernoteWidget())
