import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scope = SpotifyOAuth(scope=scope, username=username)
spotify = spotify.Spotify(auth_manager=token)
playlist_name= input("Add a playlist name: ")
playlsit_description: input("Say something about the playlist: ")

spotify/user_playlist_create(user=username, name=playlist_name, public=True, playlist_description=playlist_description )
user_input = ''
user:
wesgfweg