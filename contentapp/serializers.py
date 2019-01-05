from rest_framework import serializers
from contentapp.models import UserSignup,UserStoryTitle,UserPoem,UserBlogTitle,UserStory


class UserSignup_Serializer(serializers.ModelSerializer):

	class Meta:
		model = UserSignup
		fields = ('full_name', 'email','phone_number','city','state','country','short_description','user_photo','cover_photo')


class UserStoryTitleSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserStoryTitle
		fields = ('id','title', 'short_description','search_by','default_image')

class UserStorySerializer(serializers.ModelSerializer):

	class Meta:
		model = UserStory
		fields = ('id','content','story_seen_no')

class UserBlogTitleSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserBlogTitle
		fields = ('id','title', 'short_description','search_by','default_image')

class UserPoemSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserPoem
		fields = ('id','title', 'short_description','search_by','default_image','content')
