from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Post(models.Model):
    postText = models.CharField(max_length=100)
    pubDate = models.DateField()
    publisherName = models.CharField(max_length=20)
    numOfComments = models.IntegerField()

    def __str__(self):
        return self.publisherName


class Comment(models.Model):
    comText = models.CharField(max_length=100)
    comDate = models.DateField()
    comPubName = models.CharField(max_length=20)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)

    def __str__(self):
        return self.comPubName


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

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()



