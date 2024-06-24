from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userid = models.IntegerField()
    bio = models.TextField(max_length=400, blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_images/files', default='default_profile_img.png')
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user_id} - {self.user.username}"
    