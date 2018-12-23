from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

class UserSignup(models.Model):
    full_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=70)
    password = models.EmailField(max_length=70,null=True,blank=True)
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}')
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    city  = models.CharField(max_length=15,null=True,blank=True)
    state  = models.CharField(max_length=15,null=True,blank=True)
    country = models.CharField(max_length=15,default='India')
    short_description  = models.CharField(max_length=255,null=True,blank=True)
    user_photo = models.ImageField(null=True, blank=True, upload_to="imgae_path/")
    cover_photo = models.ImageField(null=True, blank=True, upload_to="imgae_path/")
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.full_name

class LoggingHistory(models.Model):
    user_url = models.CharField(max_length=255,null=True,blank=True)
    user_hits = models.BigIntegerField(default=0)
    free_hits = models.BigIntegerField(default=0)
    remaining_hits = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user_url


class UserBlog(models.Model):
    blog_user = models.ForeignKey(UserSignup, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True,blank=True)
    short_description = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField()
    status = models.BooleanField(default=True)
    BLOG_CHOICES = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    )
    privacy = models.CharField(max_length=10, choices=BLOG_CHOICES, default='PUBLIC')   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class UserStory(models.Model):
    blog_user = models.ForeignKey(UserSignup, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True,blank=True)
    short_description = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField()
    status = models.BooleanField(default=True)
    STORY_CHOICES = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    )
    privacy = models.CharField(max_length=10, choices=STORY_CHOICES, default='PUBLIC')   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class UserPoem(models.Model):
    blog_user = models.ForeignKey(UserSignup, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True,blank=True)
    short_description = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField()
    status = models.BooleanField(default=True)
    POEM_CHOICES = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    )
    privacy = models.CharField(max_length=10, choices=POEM_CHOICES, default='PUBLIC')   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title











