from django.db.models import CharField

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
    relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return "%s " % self.user

    def add_relationship(self, person, status):
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status)
        return relationship

    def remove_relationship(self, person, status):
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
            status=status).delete()
        return

    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self)

    def get_related_to(self, status):
        return self.related_to.filter(
            from_people__status=status,
            from_people__to_person=self)

    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)

    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)


RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)


class Relationship(models.Model):
    from_person = models.ForeignKey(Profile,related_name='from_people')
    to_person = models.ForeignKey(Profile,related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)

    def __str__(self):
        temp = '{0.from_person} -> {0.to_person} : {0.status}'
        return temp.format(self)


class Post(models.Model):
    postText = models.CharField(max_length=100)
    pubDate = models.DateField(default=timezone.now())
    publisher = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        temp = '{0.publisher} : {0.postText}'
        return temp.format(self)

    def get_comments(self):
        post = self
        activities = Activity.objects.filter(post=post)
        comments = Comment.objects.filter(activity=activities)
        return comments

    def get_datiledPost(self):
        return DetailedPost.objects.filter(post = self)


class Tag(models.Model):
    name = models.CharField(max_length=30)
    post = models.ManyToManyField(Post)

    def __str__(self):
        temp = '{0.name} : {0.post}'
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


class DetailedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True ,default=None)
    detailed = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.detailed