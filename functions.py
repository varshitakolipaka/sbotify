
import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'playlist-modify-public'
username = '6tuo5kv4t1yadwyhogmk05jon' 

token = SpotifyOAuth(scope=scope, username=username)
print("HELLOOOO0")
spotifyObject = spotipy.Spotify(auth_manager = token)
print("HELLOOOO1")
playlist_name = input("Add a playlist name ")
print("HELLOOOO2")
playlist_description = input("Say something about the playlist ")
print("HELLOOOO3")
scope = SpotifyOAuth(scope=scope, username=username)
print("HELLOOOO4")
#spotify = spotipy.Spotipy(auth_manager=token)


spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)
print("HELLOOOO5")
# user_input = ''
# user_input = input('Enter songs\' name: ')
# list_of_songs = []
# while user_input != 'quit':
# 	results = spotify.search(q=user_input)
# 	print(results['tracks']['item'][0]['uri'])

# 	newResults = results['tracks']['items'][0]['uri']

# 	list_of_songs.append(newResults)

# 	prePlaylists = spotify.user_playlists(user=username)
# 	playlist = prePlaylists['items'][0]['id']
# 	user_input = input('Enter songs\' name')

# spotify.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=list_of_songs)