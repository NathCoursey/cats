from django.db import models
import time
from django.contrib.auth.models import User

class Artist(models.Model):

    name = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    bio = models.TextField(max_length=500)
    verified_artist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Artwork(models.Model):

    title = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="artworks")

    def __str__(self):
        return self.title

    
class Artgallery(models.Model):

    title = models.CharField(max_length=150)
    artworks = models.ManyToManyField(Artwork)

    def __str__(self):
        return self.title
