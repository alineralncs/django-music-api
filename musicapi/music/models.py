from django.db import models
import pandas as pd
from django.db.models import Count


class Artist(models.Model):
    name = models.CharField(max_length=100)
    imageURL = models.URLField(null=True, blank=True, max_length=100)
    genre = models.CharField(max_length=100)

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


def apagar_artistas():
    Artist.objects.all().delete()

def  criar_artistas():
    dataset = pd.read_csv('dataset/spotify_artists_info_complete.csv', delimiter='\t')
    print('dataset', dataset)

    for index, row in dataset.iterrows():
            name_tuple=row['name'],
            name = name_tuple[0]
            imageURL=row['image_url']
            genres=row['genres']

            artist_count = Artist.objects.filter(name=name).annotate(count=Count('id')).values('count')
            if artist_count and artist_count[0]['count'] > 0:
                continue
            artist = Artist(
                name=name,
                imageURL=imageURL,
                genre=genres,
            )
            artist.save()