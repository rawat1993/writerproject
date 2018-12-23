from django.shortcuts import render,render_to_response

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from contentapp.models import UserSignup
from contentapp.serializers import UserSignup_Serializer
# Create your views here.
from django_summernote.widgets import SummernoteInplaceWidget
from contentapp.forms import UserSignupForm

class UserSignupView(APIView):

    def get(self,request):
        print('hellooo')
        queryset = UserSignup.objects.all()
        print("yeeee==>",queryset)
        # UserSignup.objects.get()
        form = UserSignupForm()
        # return render_to_response('hello.html',{'form':form,'user':queryset[0].full_name})
        return render_to_response('hello.html',{'user':queryset[0].full_name})

    def post(self,request):
    	UserSignup.objects.create(full_name='rakesh',email='rakesh@gmail.com',city='raltam',state='xyz',user_text=request.POST.get('foo'))
    	return Response('success',status=status.HTTP_200_OK)

