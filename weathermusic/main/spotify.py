import base64
import json
import os
import random
from dataclasses import dataclass

from dotenv import load_dotenv
from requests import post, get

from . import playlists

load_dotenv()

""" This classes allows to connect with spotify API and return data """


@dataclass
class SpotifyData:
    """ DATA CLASS FOR SPOTIFY ACCESS """
    CLIENT_ID: str = os.getenv('CLIENT_ID')
    CLIENT_SECRET: str = os.getenv('CLIENT_SECRET')


class SpotifyAccess(SpotifyData):
    """ This class allows to generate the token for spotify API """

    def _get_token(self):
        auth_string = f'{self.CLIENT_ID}:{self.CLIENT_SECRET}'
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

    @staticmethod
    def _get_auth_header(token: str):
        return {"Authorization": "Bearer " + token, 'Content-Type': 'application/json'}


class SpotifyCategory(SpotifyAccess):
    """ Main spotify class that can be easily extended with new methods"""

    def _search_playlist(self, token: str, playlist_id: str):
        """ This method allows to download url and other info about playlist from the API"""

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        headers = self._get_auth_header(token)
        params = {'market': 'ES'}

        result = get(url, headers=headers, params=params)
        json_result = json.loads(result.content)

        if result.status_code == 200:
            playlist_url = json_result['external_urls']['spotify']
            return playlist_url
        raise Exception("Nie działa")

    def get_random_playlist(self, token: str, weather_desc: str):
        """ This method allows to return random playlist based on the weather info """

        for weather_key in playlists.WEATHER_PLAYLISTS.keys():
            if weather_key in weather_desc:
                playlist_id = random.choice(playlists.WEATHER_PLAYLISTS[weather_key])[1]
                playlist_url = self._search_playlist(token, playlist_id)
                return playlist_url
