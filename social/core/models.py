from django.db import models
from django.contrib.auth import get_user_model
import uuid 
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userid = models.IntegerField()
    bio = models.TextField(max_length=400, blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_images/files', default='default_profile_img.png')
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.userid} - {self.user.username}"
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)     
    user =  models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    caption = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    num_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    post_id = models.CharField(max_length=250)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user