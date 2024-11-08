from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OTP(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    otp_code = models.CharField(max_length=4)  
    created_at = models.DateTimeField(auto_now_add=True)  
    
class userregister(models.Model):
    Name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='userprofile')
    bio = models.TextField(default='Add Something About Yourself...')
    profilepic = models.ImageField(upload_to='images/',blank=True, null=True)

    def __str__(self):
        return self.bio

class post(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_post')
    post_text = models.TextField(default='')
    post_pic = models.ImageField(upload_to='images/', blank=True, null=True)
    postcreated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_text
    
    