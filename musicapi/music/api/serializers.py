from rest_framework import serializers
from music.models import Artist, Music, Playlist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('url', 'id', 'name')

class MusicSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(
        queryset=Artist.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Music
        fields = ('url' ,'id', 'artist', 'name', 'duration', 'genre')

    
class PlaylistSerializer(serializers.ModelSerializer):
    music = serializers.SlugRelatedField(
        queryset= Music.objects.all(),
        slug_field='name',
        many=True
        )

    class Meta:
        model = Playlist
        fields = ('url','id', 'name', 'music')
        

