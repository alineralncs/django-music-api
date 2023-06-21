from rest_framework import serializers
from music.models import Artist, Music, Playlist, Recomendation

class MusicSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(
        queryset=Artist.objects.all(),
        slug_field='imageURL'
    )


    class Meta:
        model = Music
        fields = ('url' ,'id', 'artist', 'name', 'genre', 'subgenre' )


class ArtistSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ('url', 'id', 'name', 'imageURL', 'musics')


    
class PlaylistSerializer(serializers.ModelSerializer):
    music = MusicSerializer(many=True, required=False)
    #music = serializers.PrimaryKeyRelatedField(many=True, queryset=Music.objects.all(), required=False)

    class Meta:
        model = Playlist
        fields = ['url', 'id', 'name', 'music']
        

class RecomendationSerializer(serializers.ModelSerializer):
    playlist = PlaylistSerializer(required=False)

    class Meta:
        model = Recomendation
        fields = ['id', 'genre', 'subgenre', 'playlist']
