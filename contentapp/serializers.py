from rest_framework import serializers
from contentapp.models import UserSignup,UserStoryTitle,UserPoem,UserBlogTitle,UserStory,UserBlog


class UserSignup_Serializer(serializers.ModelSerializer):

	class Meta:
		model = UserSignup
		fields = ('full_name', 'email','phone_number','city','state','country','short_description','user_photo','cover_photo')


class UserStoryTitleSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserStoryTitle
		fields = ('id','title','published_content','short_description','search_by','default_image','title_choice','updated_at','overall_rating','total_reviewer','five_star_avg','four_star_avg','three_star_avg','two_star_avg','one_star_avg','coming_soon')

class UserStorySerializer(serializers.ModelSerializer):

	class Meta:
		model = UserStory
		fields = ('id','content','story_seen_no')

class UserBlogTitleSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserBlogTitle
		fields = ('id','title','published_content','short_description','search_by','default_image','title_choice','updated_at')

class UserBlogSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserBlog
		fields = ('id','content','blog_part')


class UserPoemSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserPoem
		fields = ('id','title','published_content','short_description','search_by','default_image','title_choice','overall_rating','total_reviewer','five_star_avg','four_star_avg','three_star_avg','two_star_avg','one_star_avg','coming_soon','updated_at')

class UserPoemContentSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserPoem
		fields = ('id','title', 'short_description','default_image','content')
