from rest_framework import serializers
from contentapp.models import UserSignup


class UserSignup_Serializer(serializers.ModelSerializer):

	class Meta:
		model = UserSignup
		fields = ('full_name', 'email')