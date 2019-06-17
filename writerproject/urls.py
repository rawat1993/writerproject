"""writerproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf.urls.static import static
from django.conf import settings
from contentapp.admin import user_admin_site
from contentapp import views,user_profile_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('super-admin/', admin.site.urls),
    path('accounts/login/', user_admin_site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('api/',include('contentapp.urls')),
    path('activate/',views.user_activation),
    path('url-postfix-availability/',views.url_postfix_availability),
    re_path(r'^(?P<post_fix_value>\w+)/$', user_profile_views.UserProfileView.as_view()),
    re_path(r'^(?P<post_fix_value>\w+)/(?P<subject>\w+)/$', user_profile_views.SubjectView.as_view()),
    re_path(r'^(?P<post_fix_value>\w+)/(?P<subject>\w+)/(?P<title>\w+)/$', user_profile_views.TitleView.as_view()),
    re_path(r'^(?P<post_fix_value>\w+)/(?P<subject>\w+)/(?P<title>\w+)/(?P<page>\w+)/$', user_profile_views.PageForTitleView.as_view()),
    path('basic-detail/', user_profile_views.TitleDetail.as_view()),
    path('about-us/', views.about_us_page),
    path('home-detail/', views.home_page_detail),
    path('rating-email/', views.rating_email),
    path('verify-otp/', views.verify_otp),
    path('rating-detail/', views.rating_detail),
    path('reviewers-detail/', views.reviewers_detail),

    # Reset Password urls
    path('account-reset-password/',auth_views.PasswordResetView.as_view(),name='admin_password_reset'),
    path('reset-password-done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path( 'reset-done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')

]

#if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
