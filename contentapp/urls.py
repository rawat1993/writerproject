from django.urls import path,include
from contentapp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'writer-profile', views.WriterProfileView)

urlpatterns = [
    path('', include(router.urls)),
    path('user-signup/',views.UserSignupView.as_view(), name='user_signup'),
]