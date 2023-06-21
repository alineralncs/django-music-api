# restframework import
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from rest_framework.decorators import action
import random
import numpy as np
import time
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
# models import
from music.models import Artist
from music.models import Music
from music.models import Playlist
from music.models import Recomendation
from music.models import apagar_artistas, apagar_musicas, apagar_musicas_duplicadas
# serializers import 
from music.api.serializers import ArtistSerializer
from music.api.serializers import MusicSerializer
from music.api.serializers import PlaylistSerializer
from music.api.serializers import RecomendationSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    '''
    Artist 
    '''
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    #pagination_class = None
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
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
     
class RecomendationViewSet(viewsets.ModelViewSet):
    '''
    Recomendacoes
    '''
    serializer_class = RecomendationSerializer
    queryset = Recomendation.objects.all()

    import time
    #dataset = pd.read_csv('dataset/dataset_musicas.csv')
    n_rows_to_read = 3000
    dataset = pd.read_csv('dataset/dataset_final.csv')

    dataset.info()
    print(dataset['playlist_genre'].head())
    print(dataset['playlist_subgenre'].head())
    print(dataset.shape)

    generos_disponiveis = dataset['playlist_genre'].unique().tolist()

    @action(detail=False, methods=['post'])
    def populate_data(self, request):
        # apagar_artistas()
        # apagar_musicas()
        apagar_musicas_duplicadas()
        # artists_created = set()
        # music_instances = []
        # for index, row in self.dataset.iterrows():
        #     artist_name = row['artistas']
        #     image = row['imagem_artista_url']
        #     if artist_name not in artists_created:
        #         try:
        #             artist = Artist.objects.get(name=artist_name)
        #         except Artist.DoesNotExist:
        #             artist = Artist.objects.create(name=artist_name, imageURL=image)
        #             artists_created.add(artist_name)
        #     else:
        #         artist = Artist.objects.get(name=artist_name)

        #     music = Music(
        #         artist=artist,
        #         name=row['track_name'],
        #         genre=row['playlist_genre'],
        #         subgenre=row['playlist_subgenre']
        #     )
        #     music_instances.append(music)

        # Music.objects.bulk_create(music_instances)

        return Response({"message": "Data populated successfully."})

    

    # Measure the execution time of a specific step

    def create(self, request, *args, **kwargs):
        # Obtenha os dados fornecidos pelo usuário
        #genero = request.data.get('genero')
        #subgenero = request.data.get('subgenero')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        genero = serializer.validated_data.get('genre')
        subgenero = serializer.validated_data.get('subgenre')
        #nome_playlist = serializer.validated_data.get('name')

        print(self.dataset.isnull().any())
        X = self.dataset[['playlist_genre', 'playlist_subgenre', 'track_name', 'artistas']]
        

        label_encoder_genre = LabelEncoder()
        label_encoder_subgenre = LabelEncoder()

        X_encoded = X.copy()
        X_encoded['playlist_genre'] = label_encoder_genre.fit_transform(X_encoded['playlist_genre'])
        X_encoded['playlist_subgenre'] = label_encoder_subgenre.fit_transform(X_encoded['playlist_subgenre'])

        # Remover a coluna 'track_name'
        X_encoded_no_track = X_encoded[['playlist_genre', 'playlist_subgenre']]

        encoder = OneHotEncoder()
        X_encoded_no_track = encoder.fit_transform(X_encoded_no_track)
        print('x', X_encoded_no_track)
        num_clusters = 10
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)

        kmeans.fit(X_encoded_no_track)


        new_playlist_genre = label_encoder_genre.transform([genero])
        new_playlist_subgenre = label_encoder_subgenre.transform([subgenero])

        new_playlist_genre_encoded = encoder.transform([[new_playlist_genre[0], new_playlist_subgenre[0]]]).toarray()

        # cluster_label = kmeans.predict(new_playlist_genre_encoded)
        cluster_label = kmeans.predict(new_playlist_genre_encoded)

        # Filtrar os exemplos no conjunto de dados original que pertencem ao cluster identificado
        cluster_samples = X[kmeans.labels_ == cluster_label[0]]

        num_recommendations = 10
        recommendations = cluster_samples.sample(n=num_recommendations)[['track_name', 'playlist_genre', 'playlist_subgenre', 'artistas']]
        

        # Add the playlist to the recommendation instance
        playlist = Playlist.objects.create(name="For you")

        for _, row in recommendations.iterrows():
            artist_name = row['artistas']
            
            # Check if the artist already exists in the database
            artist, _ = Artist.objects.get_or_create(name=artist_name)
            
            music = Music.objects.create(
                name=row['track_name'],
                genre=row['playlist_genre'],
                subgenre=row['playlist_subgenre'],
                artist=artist
            )
            playlist.music.add(music)

        recomendation = Recomendation.objects.create(genre=genero, subgenre=subgenero, playlist=playlist)
        #recomendation.playlist = playlist
        recomendation.save()



        # Prepare the response data
        response_data = {
            'id': recomendation.id,
            'genre': recomendation.genre,
            'subgenre': recomendation.subgenre,
            'playlist': {
                'id': playlist.id,
                'name': playlist.name,
                'music': list(playlist.music.values('id', 'name', 'genre', 'subgenre')),
            },
        }

        # Return the response
        return Response(response_data)


  
