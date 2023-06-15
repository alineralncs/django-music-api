from django.db import models
import pandas as pd

class Artist(models.Model):
    name = models.CharField(max_length=100)
    imageURL = models.URLField(null=True, blank=True, max_length=100)
    
    class Meta:
        ordering = ['id']

    def __str__ (self):
        return self.name 

class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
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


def  criar_artistas():
    dataset = pd.read_csv('dataset/spotify_artists_info_complete.csv', delimiter='\t')
    print('dataset', dataset)

    for index, row in dataset.iterrows():
            artist = Artist(
                name=row['name'],
                imageURL=row['image_url']
            )

            artist.save()