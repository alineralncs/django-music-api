# restframework import
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
# models import
from music.models import Artist
from music.models import Music
from music.models import Playlist
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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
     

