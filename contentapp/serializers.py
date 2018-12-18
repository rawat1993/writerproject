from rest_framework import serializers
from contentapp.models import WriterProfile

class WriterProfile_Serializer(serializers.ModelSerializer):

	class Meta:
		model = WriterProfile
		fields = ('first_name', 'last_name', 'template_render')
