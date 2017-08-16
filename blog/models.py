from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return "%s " % self.user


class Post(models.Model):
    postText = models.CharField(max_length=100)
    pubDate = models.DateField(default=timezone.now())
    publisher = models.ForeignKey(Profile , on_delete=models.CASCADE,null=True ,default=None)

    def __str__(self):
        temp = '{0.publisher} : {0.postText}'
        return temp.format(self)


class Activity(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True ,default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True ,default=None)

    def __str__(self):
        temp = '{0.post} <=> {0.user}'
        return temp.format(self)


class Comment(models.Model):
    comText = models.CharField(max_length=100)
    comDate = models.DateField(default=timezone.now())
    activity = models.ForeignKey(Activity , on_delete=models.CASCADE,null=True ,default=None)

    def __str__(self):
        temp = '{0.comText}'
        return temp.format(self)


class Like(models.Model):
    activity = models.ForeignKey(Activity , on_delete=models.CASCADE,null=True ,default=None)
    likeDate = models.DateField(default=timezone.now())

    def __str__(self):
        temp = '{0.activity}'
        return temp.format(self)


class Bookmark(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,null=True ,default=None)
    bookmarkDate = models.DateField(default=timezone.now())

    def __str__(self):
        temp = '{0.activity}'
        return temp.format(self)


class Share(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,null=True ,default=None)
    shareDate = models.DateField(default=timezone.now())

    def __str__(self):
        temp = '{0.activity}'
        return temp.format(self)


class FollowerOf(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, default=None)
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, default=None)
    startDate = models.DateField(timezone.now())

