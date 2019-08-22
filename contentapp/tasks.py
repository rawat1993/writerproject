from writerproject.celery import app
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .constants import *

def send_email(subject, send_message, toUser):
    """
    Send email function
    """

    text_content = strip_tags(send_message)
    msg = EmailMultiAlternatives(
        subject, text_content, 'writercreativity612@gmail.com', toUser)
    msg.attach_alternative(send_message, "text/html")
    msg.send()

@app.task
def sent_notictaion_email_to_author(page_type,search_by,name,star_value,page_title):
    if page_type=="story":
        obj = UserStoryTitle.objects.get(search_by=search_by)
    elif page_type=="poem":
        obj = UserPoem.objects.get(search_by=search_by)
    
    notification_status = obj.notification
    if notification_status=="ON":
        try:
            page_title = page_title.title()
            name = name.title()
            first_name = (name.split()[0]).title()
            author_email = obj.author.email
            author_name = UserSignup.objects.get(email=author_email).full_name.split()[0]    
            author_url = UrlPostfixHistory.objects.get(user_email=author_email).url_postfix

            html_content = render_to_string('mail_template.html', {'var_name': author_name.title(), 'body_content':NOTIFICATION_EMAIL.format(name,page_type,page_title,first_name,star_value), 'terms_conditions':REVIEWER_LINK.format(author_url,page_type,search_by)})
            
            send_email(NOTIFICATION_SUBJECT.format(page_title,name), html_content, [author_email])
        except Exception as e:
            print("error",e)

@app.task
def sent_notification_email_to_WC(published_content):
        try:
            send_email("Please Verify Published Data", published_content, ["rawatajay977@gmail.com"])
        except Exception as e:
            pass