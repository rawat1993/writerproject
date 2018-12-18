from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

class WriterProfile(models.Model):
    first_name = models.CharField(max_length=15)
    last_name  = models.CharField(max_length=15)
    email = models.EmailField(max_length=70,blank=True)
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}')
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)   
    short_description  = models.TextField()
    city  = models.CharField(max_length=15)
    state  = models.CharField(max_length=15)
    country = models.CharField(max_length=15)

    ZENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )
    zender = models.CharField(max_length=10, choices=ZENDER_CHOICES)
    status = models.BooleanField(default=True)
    front_end_code = models.TextField()
    template_render = models.TextField()
    def __str__(self):
        return self.first_name
