# restframework import
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

import numpy as np
import time
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
# models import
from music.models import Artist
from music.models import Music
from music.models import Playlist
from music.models import Recomendacao
from music.models import apagar_artistas, apagar_musicas
# serializers import 
from music.api.serializers import ArtistSerializer
from music.api.serializers import MusicSerializer
from music.api.serializers import PlaylistSerializer
from music.api.serializers import RecomendacaoSerializer

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
     
class RecomendacaoViewSet(viewsets.ModelViewSet):
    '''
    Recomendacoes
    '''
    serializer_class = RecomendacaoSerializer
    queryset = Recomendacao.objects.all()

    import time
    #dataset = pd.read_csv('dataset/dataset_musicas.csv')
    n_rows_to_read = 3000
    dataset = pd.read_csv('dataset/dataset_musicas.csv', nrows=n_rows_to_read)

    dataset.info()
    print(dataset['playlist_genre'].head())
    print(dataset['playlist_subgenre'].head())
    print(dataset.shape)

    generos_disponiveis = dataset['playlist_genre'].unique().tolist()

    def populate_data(self):
        artists_created = set()
        for index, row in self.dataset.iterrows():
            artist_name = row['artistas']
            image = row['imagem_artista_url']
            if artist_name not in artists_created:
                artist = Artist.objects.create(name=artist_name, imageURL=image)
                artists_created.add(artist_name)

            artist = Artist.objects.get(name=artist_name)

            music = Music.objects.create(
                artist=artist,
                name=row['track_name'],
                genre=row['playlist_genre'],
                subgenre=row['playlist_subgenre']
            )
    

    # Measure the execution time of a specific step

    def create(self, request, *args, **kwargs):
        # Obtenha os dados fornecidos pelo usuário
        #genero = request.data.get('genero')
        #subgenero = request.data.get('subgenero')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        genero = serializer.validated_data.get('genre')
        subgenero = serializer.validated_data.get('subgenre')

        print(self.dataset.isnull().any())
        # Filtrar o dataset com base no gênero e subgênero fornecidos
        start_time = time.time()

        # Separar as variáveis de entrada (features) e saída (target)
        X = self.dataset[['playlist_genre', 'playlist_subgenre']]
        y = self.dataset['track_name']  # Coluna que representa as músicas
        
        print(X.shape)
        print(y.shape)
        label_encoder = LabelEncoder()
        X_encoded = X.apply(label_encoder.fit_transform)
        
        y_encoded = label_encoder.fit_transform(y)
       
        # Treinar o modelo MLPClassifier
        model = MLPClassifier(hidden_layer_sizes=(100, 100), verbose=True, activation='relu', solver='adam', random_state=42)
        #model = DecisionTreeClassifier(random_state=42)

        model.fit(X_encoded, y_encoded)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

        num_recomendacoes = 10 # Exemplo: gerar 5 recomendações
        genero_numeric = int(genero)
        subgenero_numeric = int(subgenero)

        # Gerar as recomendações com base nos dados fornecidos pelo usuário
        user_data = [[genero_numeric, subgenero_numeric]] 
        print('user data', user_data) # Dados fornecidos pelo usuário
        #user_data_encoded = label_encoder.transform(user_data)
        # user_data_encoded = [label_encoder.transform([genero])[0], label_encoder.transform([subgenero])[0]]
        # print('user data encoded', user_data_encoded)
        recommendations = model.predict(user_data)
        recommendations = recommendations[:num_recomendacoes]  # Keep only the first 10 recommendations

        # print('recommendations_encoded', recommendations)

        # Reverter o processo de codificação para obter as recomendações como strings
        #recommendationsss = label_encoder.inverse_transform(recommendations_encoded)
        print('recommendations',recommendations )
        # Prepare data to be serialized
        recomendacao = Recomendacao.objects.create( 
            genre= genero,
            subgenre= subgenero,
            music= recommendations.tolist()
        )

        serializer = self.get_serializer(recomendacao)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


        # # Criar uma instância de RecommendedMusic para cada recomendação gerada
        # for recommendation in recommendations[:num_recomendacoes]:
        #         recommended_music = Recomendacao.objects.create(
        #             genre=genero,
        #             subgenre=subgenero,
        #             music=recommendation
        #         )
        #         recommended_music.save()

    # @action(detail=False, methods=['post'])
    # def criar_artistas(self, request):
    #     self.populate_data()
    #     # apagar_artistas()
    #     # apagar_musicas()
    #     return Response({"message": "Artistas criados com sucesso."})