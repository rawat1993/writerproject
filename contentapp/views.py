from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from contentapp.models import WriterProfile
from contentapp.serializers import WriterProfile_Serializer
# Create your views here.


class WriterProfileView(viewsets.ViewSet):
    queryset = WriterProfile.objects.all()
    serializer_class = WriterProfile_Serializer

    def list(self,request):
        serializer = WriterProfile_Serializer(self.queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
