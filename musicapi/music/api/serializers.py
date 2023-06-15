from rest_framework import serializers
from music.models import Artist, Music, Playlist

class MusicSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(
        queryset=Artist.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Music
        fields = ('url' ,'id', 'artist', 'name', 'duration', 'genre', 'lyrics')


class ArtistSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ('url', 'id', 'name', 'imageURL', 'musics')


    
class PlaylistSerializer(serializers.ModelSerializer):
    music = MusicSerializer(many=True, required=False)
    # serializers.SlugRelatedField(
    #     queryset= Music.objects.all(),
    #     slug_field='name',
    #     many=True
    #     )

    class Meta:
        model = Playlist
        fields = ('url','id', 'name', 'imageURL', 'music')
        

