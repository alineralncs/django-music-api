# restframework import
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response


# models import
from music.models import Artist
from music.models import Music
from music.models import Playlist
from music.models import criar_artistas
# serializers import 
from music.api.serializers import ArtistSerializer
from music.api.serializers import MusicSerializer
from music.api.serializers import PlaylistSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    '''
    Artist 
    '''
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    #pagination_class = None

    
    @action(detail=False, methods=['post'])
    def criar_artistas(self, request):
        criar_artistas()
        return Response({"message": "Artistas criados com sucesso."})

class MusicViewSet(viewsets.ModelViewSet):
    '''
    Music
    '''
    serializer_class = MusicSerializer
    queryset = Music.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class PlaylistViewSet(viewsets.ModelViewSet):
    '''
    Playlist
    '''
    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
     

