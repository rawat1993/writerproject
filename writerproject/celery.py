from celery import Celery, Task
import urllib.request
import os
from django.conf import settings

# Where the downloaded files will be stored
BASEDIR="/home/celery/downloadedFiles"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'writerproject.settings')
# Create the app and set the broker location (RabbitMQ)
app = Celery('writerproject',
             broker='amqp://guest@localhost:5672//')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)