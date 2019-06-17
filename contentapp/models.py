from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.

class UserSignup(models.Model):
    full_name = models.CharField(help_text="you can edit your name",max_length=30)
    email = models.EmailField(max_length=70,unique=True)
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}')
    phone_number = models.CharField(help_text="enter your mobile number",validators=[phone_regex], max_length=17, null=True,blank=True)
    city  = models.CharField(max_length=15,null=True,blank=True)
    state  = models.CharField(max_length=15,null=True,blank=True)
    country = models.CharField(max_length=15,default='India')
    short_description  = models.CharField(help_text="write somthing about you",max_length=255,null=True,blank=True)
    user_photo = models.ImageField(help_text="upload your photo to see in your public profile",null=True, blank=True, upload_to="imgae_path/")
    cover_photo = models.ImageField(help_text="upload your cover photo",null=True, blank=True, upload_to="imgae_path/")
    status = models.BooleanField(default=False,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    class Meta:
        verbose_name_plural = 'Click here to edit your profile'

class UrlPostfixHistory(models.Model):
    user_email = models.CharField(max_length=70,null=True,blank=True)
    url_postfix = models.CharField(max_length=30,null=True,blank=True)
    URL_POSTFIX_STATUS = (
        ('BLOCK', 'Blocked'),
        ('UNBLOCK', 'Active'),
    )
    status = models.CharField("Super admin Action",max_length=10, choices=URL_POSTFIX_STATUS, default='UNBLOCK')
    url_postfix_status = models.BooleanField(default=False,editable=False)
    action_taken_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True,editable=False)
    def __str__(self):
        return self.user_email

class LoggingHistory(models.Model):
    user_url = models.CharField(max_length=255,null=True,blank=True,unique=True)
    user_hits = models.BigIntegerField(default=0)
    free_hits = models.BigIntegerField(default=0)
    remaining_hits = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user_url


class UserBlogTitle(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,editable=False)
    search_by = models.CharField(max_length=20,null=True,blank=True,editable=False)
    title = models.CharField('Blog Title',max_length=255,unique=True,help_text='write your blog title')
    short_description = models.CharField(max_length=255,null=True,blank=True,help_text="write short description about your Blog")
    default_image = models.ImageField(help_text="set default image for your blog", upload_to="imgae_path/")
    title_status = models.BooleanField(help_text="set false if you dont want to show title with your default image",default=True)
    BLOG_CHOICES = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    )
    privacy = models.CharField(max_length=10, choices=BLOG_CHOICES, default='PUBLIC')
    total_hits = models.BigIntegerField('Total hits for this Blog',default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Add Blog Title First'


class UserBlog(models.Model):
    title = models.ForeignKey(UserBlogTitle,on_delete=models.CASCADE,verbose_name = 'Select Your Blog')
    blog_part = models.CharField("Heading",max_length=25,help_text='write heading for this blog -> Maximum 25 characters allowed')
    content = models.TextField('Write Your Blog',help_text='Write your blog using images')
    total_hits = models.BigIntegerField('Total hits for this page',default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blog_part
    class Meta:
        unique_together = (("title", "blog_part"),)
        verbose_name_plural = 'Add Blog Content'

class UserStoryTitle(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,editable=False)
    search_by = models.CharField(max_length=20,null=True,blank=True,editable=False)
    title = models.CharField('Story Title',max_length=100,unique=True,help_text='write your story title')
    short_description = models.CharField('Story Short Description',max_length=255,null=True,blank=True,help_text='Write short description about your story')
    default_image = models.ImageField(help_text="set default image for your story", upload_to="imgae_path/")
    title_status = models.BooleanField(help_text="set false if you dont want to show title with your default image",default=True)
    STORY_CHOICES = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    )
    privacy = models.CharField(max_length=10, choices=STORY_CHOICES, default='PUBLIC')
    total_hits = models.BigIntegerField('Total hits for this Stroy',default=0)

    one_star_count = models.IntegerField(default=0,editable=False)
    two_star_count = models.IntegerField(default=0,editable=False)
    three_star_count = models.IntegerField(default=0,editable=False)
    four_star_count = models.IntegerField(default=0,editable=False)
    five_star_count = models.IntegerField(default=0,editable=False)
    total_reviewer = models.IntegerField(default=0,editable=False)

    one_star_avg = models.IntegerField(default=0,editable=False)
    two_star_avg = models.IntegerField(default=0,editable=False)
    three_star_avg = models.IntegerField(default=0,editable=False)
    four_star_avg = models.IntegerField(default=0,editable=False)
    five_star_avg = models.IntegerField(default=0,editable=False)
    overall_rating = models.FloatField(default=0.0,editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Add Stroy Title First'

class UserStory(models.Model):
    title = models.ForeignKey(UserStoryTitle, on_delete=models.CASCADE,verbose_name = 'Select Your Story')
    story_seen_no = models.CharField('Heading',max_length=25,help_text='write a heading for this scene -> Maximum 25 characters allowed')
    content = models.TextField('Write Your Story',help_text='Write your stroy seen using images')
    total_hits = models.BigIntegerField('Total hits for this page',default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.story_seen_no
    class Meta:
        unique_together = (("title", "story_seen_no"),)
        verbose_name_plural = 'Add Stroy Content'

class UserPoem(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,editable=False)
    search_by = models.CharField(max_length=20,null=True,blank=True,editable=False)
    title = models.CharField('Poem Title',max_length=100,unique=True,help_text='write your poem title')
    title_status = models.BooleanField(help_text="set false if you dont want to show title with your default image",default=True)
    short_description = models.CharField('Poem Short Description',max_length=255,null=True,blank=True,help_text='Write short description about your poem')
    default_image = models.ImageField(help_text="set default image for your poem", upload_to="imgae_path/")    
    content = models.TextField('Write Your Poem',help_text='Write your poem using images')
    POEM_CHOICES = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    )
    privacy = models.CharField(max_length=10, choices=POEM_CHOICES, default='PUBLIC')
    total_hits = models.BigIntegerField('Total hits for this poem',default=0)

    one_star_count = models.IntegerField(default=0,editable=False)
    two_star_count = models.IntegerField(default=0,editable=False)
    three_star_count = models.IntegerField(default=0,editable=False)
    four_star_count = models.IntegerField(default=0,editable=False)
    five_star_count = models.IntegerField(default=0,editable=False)
    total_reviewer = models.IntegerField(default=0,editable=False)

    one_star_avg = models.IntegerField(default=0,editable=False)
    two_star_avg = models.IntegerField(default=0,editable=False)
    three_star_avg = models.IntegerField(default=0,editable=False)
    four_star_avg = models.IntegerField(default=0,editable=False)
    five_star_avg = models.IntegerField(default=0,editable=False)
    overall_rating = models.FloatField(default=0.0,editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Add Poem'


class AboutUs(models.Model):
    about_us = models.CharField(max_length=200,null=True,blank=True)
    content = models.TextField('Add about-us page',help_text='Add about-us content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.about_us
    class Meta:
        verbose_name_plural = 'Add About-Us'

class Rating(models.Model):
    rate_by = models.CharField(max_length=100)
    user_name = models.CharField(max_length=50,null=True,blank=True)
    rating_value = models.IntegerField(default=0)
    rated_title = models.CharField(max_length=50)
    comment = models.TextField(null=True,blank=True)
    block_this_comment = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rate_by
    class Meta:
        verbose_name_plural = 'Rating'

class FakeRaters(models.Model):
    email = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    action_taken_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural = 'Fake Raters'

class EmailOTP(models.Model):
    email = models.CharField(max_length=100)
    otp_number = models.IntegerField(default=0)
