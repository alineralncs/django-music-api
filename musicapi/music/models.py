from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['id']

    def __str__ (self):
        return self.name 

class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration = models.TimeField()
    genre = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class Playlist(models.Model):
    music = models.ManyToManyField(Music)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.name
