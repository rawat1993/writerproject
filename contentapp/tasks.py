from background_task import background

@background(schedule=60)
def sent_notictaion_email_to_author(page_type,search_by,name,star_value,page_title):
    print("yessssssssssssssssssssssssssssssssss")
    if page_type=="story":
        obj = UserStoryTitle.objects.get(search_by=search_by)
    elif page_type=="poem":
        obj = UserPoem.objects.get(search_by=search_by)

    notification_status = obj.notification
    if notification_status=="ON":
        page_title = page_title.title()
        name = name.title()
        first_name = (name.split()[0]).title()
        author_email = obj.author.email
        author_name = UserSignup.objects.get(email=author_email).full_name.split()[0]    
        author_url = UrlPostfixHistory.objects.get(user_email=author_email).url_postfix

        html_content = render_to_string('mail_template.html', {'var_name': author_name.title(), 'body_content':NOTIFICATION_EMAIL.format(name,page_type,page_title,first_name,star_value), 'terms_conditions':REVIEWER_LINK.format(author_url,page_type,search_by)})
        send_email(NOTIFICATION_SUBJECT.format(page_title,name), html_content, [author_email])

# def task_for_notification():
# 	sent_notictaion_email_to_author(page_type,search_by,name,star_value,page_title)
