from rest_framework import status
from rest_framework.test import APITestCase
from .models import Artist
from .models import Music
from .models import Playlist

class TestArtist(APITestCase):
    url = "/api/artist/"

    def setUp(self):
        Artist.objects.create(name="Niall")

    def test_can_list_artist(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_create_artist(self):
        data = {
            "name": "Niall",
        }

        response = self.client.post(self.url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result["name"], "Niall")
       
    def test_can_update_artist(self):
        pk = "1"
        data = {
            "name": "Niall"
        }

        response = self.client.patch(self.url + f"{pk}/", data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result["name"], "Niall")

    def test_can_delete_artist(self):
        pk = "1"

        response = self.client.delete(self.url + f"{pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TestMusic(APITestCase):
    url = "/api/music/"

    def setUp(self):
        artist = Artist.objects.create(name="Niall")
        Music.objects.create(artist=artist, name="Grapejuice", duration="00", genre="pop")

    def test_can_list_music(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_create_music(self):
        data ={
            "artist": "Niall",
            "name": "Grapejuice",
            "duration": "00",
            "genre": "Pop",
        }

        response = self.client.post(self.url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result["artist"], "Niall")
        self.assertEqual(result["name"], "Grapejuice")
        self.assertEqual(result["dration"], "00")
        self.assertEqual(result["genre"], "Pop")
       
    def test_can_update_music(self):
        pk = "1"
        data = {
            "artist": "Niall",
            "name": "Grapejuice",
            "duration": "00",
            "genre": "Pop",
        }

        response = self.client.patch(self.url + f"{pk}/", data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result["artist"], "Niall")
        self.assertEqual(result["name"], "Grapejuice")
        self.assertEqual(result["dration"], "00")
        self.assertEqual(result["genre"], "Pop")

    def test_can_delete_music(self):
        pk = "1"

        response = self.client.delete(self.url + f"{pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
