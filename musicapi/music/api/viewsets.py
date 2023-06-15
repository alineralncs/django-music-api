# restframework import
from rest_framework import viewsets
from rest_framework import filters
<<<<<<< HEAD
from rest_framework.decorators import action
from rest_framework.response import Response


=======
from rest_framework.response import Response
from rest_framework import status
>>>>>>> b19fe412fdc05771d87c9507e062387f88c29815
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
     

