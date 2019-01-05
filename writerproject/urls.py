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

urlpatterns = [
    path('super-admin/', admin.site.urls),
    path('user-admin/', user_admin_site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('api/',include('contentapp.urls')),
    path('activate/',views.user_activation),
    # re_path(r'(?P<url_post_fix>\w+)(?:/(?P<subject>[\w-]+))(?:/(?P<title>[\w-]+))?/$', user_profile_views.SecondUserProfileView.as_view(),name='user-profile'),    
    re_path(r'^(?P<post_fix_value>\w+)/$', user_profile_views.UserProfileView.as_view()),
    re_path(r'^(?P<post_fix_value>\w+)/(?P<subject>\w+)/$', user_profile_views.SubjectView.as_view()),
    re_path(r'^(?P<post_fix_value>\w+)/(?P<subject>\w+)/(?P<title>\w+)/$', user_profile_views.TitleView.as_view()),
    re_path(r'^(?P<post_fix_value>\w+)/(?P<subject>\w+)/(?P<title>\w+)/(?P<seen>\w+)/$', user_profile_views.FifthUserProfileView.as_view()),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
