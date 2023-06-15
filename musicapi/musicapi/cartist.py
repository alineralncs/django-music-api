import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music.settings')
django.setup()


import pandas as pd
from models import Artist
   
dataset = pd.read_csv('./dataset/spotify_artists_info_complete.csv')
for index, row in dataset.iterrows():
        artist = Artist(
            name=row['name'],
            imageURL=row['image_url']
        )

        artist.save()