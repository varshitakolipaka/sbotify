
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='962d2f3b1b7f4a78b0fca6cd996e1a62',client_secret='184a975003e04bf9bf29f99e1c1b4525'))
# spotifyObject = spotipy.Spotify(auth_manager = token)
playlist_name = input("Add a playlist name ")
playlist_description = input("Say something about the playlist ")
# scope = SpotifyClientCredentials()
# #spotify = spotipy.Spotipy(auth_manager=token)
print(sp.current_user_playlists())

# sp.user_playlist_create(user='6tuo5kv4t1yadwyhogmk05jon', name=playlist_name, public=True, description=playlist_description)
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