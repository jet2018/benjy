from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UsageData(models.Model):
    """
    UsageData model
    """
    user = models.ForeignKey(User, related_name='user',
                             on_delete=models.CASCADE)
    facebook = models.IntegerField(default=0)
    twitter = models.IntegerField(default=0)
    instagram = models.IntegerField(default=0)
    snapchat = models.IntegerField(default=0)
    whatsapp = models.IntegerField(default=0)
    reddit = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user)
