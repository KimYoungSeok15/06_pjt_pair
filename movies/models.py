from django.db import models
from django.conf import settings
from imagekit.processors import Thumbnail, SmartResize, ResizeToFill
from imagekit.models import ProcessedImageField, ImageSpecField


class Hashtag(models.Model):
    content = models.TextField(unique=True) 

class Movie(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    thumbnail_img = ImageSpecField(    
        source='image',
        processors=[SmartResize(200,100)], 
        format='JPEG',
        options={'quality':80},       
    )
    hashtags = models.ManyToManyField(Hashtag, through='active_hashtag')

class Comment(models.Model):
    content = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               related_name='replies',)

class Active_hashtag(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)   
