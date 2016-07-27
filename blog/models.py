from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.CharField(max_length=30, default = 'anonymous')
    post = models.ForeignKey(Post, default=1)
    text = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    like = models.IntegerField(default = 0)

    def __str__(self):
        return self.text
