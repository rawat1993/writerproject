USER_EMAIL_ALREADY_EXISTS = "User already exists"
MAIL_SUCCESSFULLY_SENT = "Activation mail has been sent successfully, Please check your Email"
USER_NOT_FOUND = "User not found"
USER_REGISTERED = "User has been successfully registered"
USER_ALREADY_REGISTERED = "User already registered with us"
URL_NOT_CORRECT = "Please correct your URL"
PAGE_NOT_FOUND = "Page not found for this {}"
TITLE_NOT_FOUND = "Content is not added yet by the Author for this {}"
NOT_AVAILABLE = "{}'s are not available for this user"
#########################################
# Mail setup

MAIL_FAILD = "Mail not sent Please check your internet"
EMAIL_SUBJECTS = "Writer | Activate account"
#EMAIL_CONTENT = "Hi {}, \n\n We sent you activation link to setup your account with us.\n http://18.188.167.66:8000/activate/?token={} \n\n\n Regards,\nWriting Team"
EMAIL_CONTENT = "Welcome to WC! To complete your registration, Please click the link below to validate your email and begin using the platform. \n\n"
ACTIVATION_LINK = "http://writercreativity.com:8000/activate/?token={}"

############## User Profile List #################
USER_POSTFIX_NOT_FOUND = "User Postfix String not found"
POSTFIX_STATUS = "You are Blocked by Admin Please contact to WC Team"

############# Fix keywords value #################
STORY = "story"
BLOG = "blog"
POEM = "poem"


############# Url PostFix Availability Message ################
POSTFIX_NOT_AVAILABLE = "not available"
AVAILABLE = "available"

################# Added IP and Port Detail ####################
IP = '18.188.167.66'
PORT = '8000'

##############################################################
HOST_NAME = 'http://18.188.167.66:8000'

######################################################
EMAIL_TOKEN_EXP_IN_SECONDS = 7776000  # token will be exprire in 90 days
TOKEN_EXPIRE = "Token has been expired"

######################### SALT SETTINGS FOR GENERATE TOKEN ################
SALT = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+~"

#####################################################################
USER_NAME="Username: {}"
PASSWORD="Password: {}"
ADMIN_LOGIN="http://www.writercreativity.com:8000/accounts/login/login/?next=/accounts/login/"
USER_PROFILE="http://writercreativity.com/{}/"

##############################################################
ABOUT_US="Content not found for about-us page"

########################### Desktop Home page constants #####################
DESKTOP_COVER_IMAGE_3 = "http://writercreativity.com:8000/media/desktop/home_page_3.jpg"
DESKTOP_COVER_IMAGE_4 = "http://writercreativity.com:8000/media/desktop/home_page_4.jpg"
DESKTOP_COVER_IMAGE_8 = "http://writercreativity.com:8000/media/desktop/home_page_8.jpg"
DESKTOP_COVER_IMAGE_9 = "http://writercreativity.com:8000/media/desktop/home_page_9.jpg"

HOME_QUOTE_1 = ["Creativity is an art","And","Art is my passion"]
HOME_QUOTE_2 = ["Sometimes you want","Read","Think a lot","But","Your responsibilities are disturb You"]
HOME_QUOTE_3 = ["I am Alone","Like","A Moon"]
HOME_QUOTE_4 = ["I am writing","About someone","Please don't tell Her"]
TEXT_COLORE_1 = "#000"
TEXT_COLOR_WHITE = "#FFF"

########################### Mobile Home page constants #####################
MOBILE_COVER_IMAGE_1 = "http://writercreativity.com:8000/media/mobile/home_image.jpg"
MOBILE_COVER_IMAGE_2 = "http://writercreativity.com:8000/media/mobile/home_image_2.jpg"
MOBILE_COVER_IMAGE_3 = "http://writercreativity.com:8000/media/mobile/home_page_3.jpg"
MOBILE_COVER_IMAGE_4 = "http://writercreativity.com:8000/media/mobile/home_page_4.jpg"
MOBILE_COVER_IMAGE_5 = "http://writercreativity.com:8000/media/mobile/home_page_5.jpg"
MOBILE_COVER_IMAGE_6 = "http://writercreativity.com:8000/media/mobile/home_page_6.jpg"
MOBILE_COVER_IMAGE_7 = "http://writercreativity.com:8000/media/mobile/home_page_7.jpg"
MOBILE_COVER_IMAGE_9 = "http://writercreativity.com:8000/media/mobile/home_page_9.jpg"

MOBILE_QUOTE_1 = ["Creativity is an art","And","Art is my passion"]
MOBILE_QUOTE_2 = ["Don't disturb Me","I am reading","My Past"]
MOBILE_COLORE_1 = "#000"



########################### Rating constants ##################################
FAKE_USER = "Your Email has been blocked By WC Team Please contact to WC"
SENT_OTP = "OTP sent to your Email Please verify"
SUBJECT_FOR_OTP = "One Time Password(OTP)"
SENT_EMAIL_WITH_OTP = "Your One Time Password(OTP) is {} \n\n You can use it to rate {}"
OTP_VALIDATED = "validated"
NOT_VALIDATE = "! Please enter correct OTP"
ALREADY_RATED = "You already rated {}"
OTP_ISSUE = "You requested for new OTP from other terminal, Please refresh the page"
RATING_SAVED = "Thanks for giving your valuable time to rate {}"
SELF_RATING = "Self rating is not Allowed"


########################## Content Verify Email constants #######################
COPYRIGHT_EMAIL = "Your content was found copied from other user content. It is against term & condition of WC. So your {} {} is blocked by WC Team. Please go through the below link to read Terms & Conditions."
SEXUAL_CONTENT_EMAIL = "We found You are using sexual content. It is against term & condition of WC. So your {} {} is blocked by WC Team. Please go through the below link to read Terms & Conditions."
ACTIVE_CONTENT_EMAIL = "Congratulation now your content is correct. And your {} {} is activated by WC Team. Please go through the below link to read Terms & Conditions."
SUBJECT_FOR_VERIFY_CONTENT = "Verified Content by WC"

######################### URLPostFix blocked Email ##############################
POSTFIX_BLOCKED_EMAIL = "Your account has been blocked by WC Team, Please go through the below link to read Terms & Conditions."
WC_TERMS_AND_CONDTIONS = "http://writercreativity.com/about-us"
POSTFIX_REACTIVATE_EMAIL = "Congratulation Your account has been re-activated by WC Team."
SUBJECT_FOR_POSTFIX_BLOCKED_EMAIL = "Account has been Blocked By WC"
SUBJECT_FOR_REACTIVATE_POSTFIX = "Congratulations your account reactivated by WC"

######################### Writer Listing Page Constant ###########################
STORY_WRITERS = "Story Writers Not Available"
POETS = "Poets are not Available"
NO_WRITERS = "No Writers Available Yet"


######################### Reviewer Notification Constant for Author ###########################
NOTIFICATION_EMAIL = "{} recently reviewed your {} {}. {} left feedback with rating of {} star, for more detail please click on below link."
NOTIFICATION_SUBJECT = "{} Reviewed by {} | WC"
REVIEWER_LINK = "http://writercreativity.com/{}/{}/{}/reviews"

######################### Home Page Headings Constant for Poem and Story #####################
POEM_HEADING = "Poem of the Week"
POEM_SUBJECT = "Poetry is when an emotion has found its thought And the thought has found Words"
POEM_SUBJECT_BY = "by Robert Frost"

STORY_HEADING = "Story of the Week"
STORY_SUBJECT = "Readers are the ink of the pen to Write"
STORY_SUBJECT_BY = "by Ajay Pal Singh"
