from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from AJKapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', index, name='homepage'),
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('logout', logoutmethod, name='logout'),
    path('otp/<int:user_id>', otpverify, name='otp'),
    path('profile', profile, name='profile'),
    path('addinfo', addinfo, name='addinfo'),
    path('editinfo', editinfo, name='editinfo'),
    path('friends', friends, name='friends'),
    path('addpost', add_post, name='addpost'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
