from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    imageURL = models.URLField(null=True, blank=True, max_length=100)
    
    class Meta:
        ordering = ['id']

    def __str__ (self):
        return self.name 

class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='musics')
    name = models.CharField(max_length=100)
    duration = models.TimeField()
    genre = models.CharField(max_length=100)
    lyrics = models.TextField(null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class Playlist(models.Model):
    music = models.ManyToManyField(Music)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True)
    imageURL = models.URLField(null=True, blank=True, max_length=100)


    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.name
