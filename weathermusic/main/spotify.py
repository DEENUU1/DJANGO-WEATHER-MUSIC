from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# This function returns API token


def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
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


def get_auth_header(token):
    return {"Authorization": "Bearer " + token, 'Content-Type': 'application/json'}

# This function returns the playlist info based on the playlist id
# Playlist description, url and image


def search_playlist(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)
    params = {'market': 'ES'}

    result = get(url, headers=headers, params=params)
    json_result = json.loads(result.content)
    if result.status_code == 200:
        playlist_title = json_result['description']
        playlist_url = json_result['external_urls']['spotify']
        playlist_image = json_result['images'][0]['url']
        return playlist_title, playlist_url, playlist_image
    else:
        print("Nie działa")
