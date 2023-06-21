from django.db import models
import pandas as pd
from django.db.models import Count


class Artist(models.Model):
    name = models.CharField(max_length=100)
    imageURL = models.URLField(null=True, blank=True, max_length=100)
    #genre = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__ (self):
        return self.name 

class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='musics')
    name = models.CharField(max_length=100)
    #duration = models.TimeField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    subgenre = models.CharField(max_length=100, blank=True, null=True)
    #lyrics = models.TextField(null=True)

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

class Recomendation(models.Model):
    genre = models.CharField(max_length=100)
    subgenre = models.CharField(max_length=100)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return f"Recomendation for {self.genre} - {self.subgenre}"

def apagar_artistas():
    Artist.objects.all().delete()


def apagar_musicas():
    Music.objects.all().delete()

def apagar_musicas_duplicadas():
    duplicatas = Music.objects.values('name').annotate(name_count=Count('name')).filter(name_count__gt=1)

    for duplicata in duplicatas:
        nome = duplicata['name']
        musicas_duplicadas = Music.objects.filter(name=nome)
        musicas_duplicadas.exclude(pk=musicas_duplicadas.first().pk).delete()
