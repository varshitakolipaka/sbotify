import os
import re
from typing import Hashable

from spotifyclient import SpotifyClient

def main(query,playlist_name):
    print("HELLLLLOOOOOOOOOOOOOO")
    #import environment variables from .env
    spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"),
                                   os.getenv("SPOTIFY_USER_ID"))
    # replace spaces with %20
    query = query.replace(" ","%20")
    # using the function "get_track"
    added_song = spotify_client.get_track(query)
    print("--------------------------------------")
    print("OMFGGGG LOOK AT THIS:   ",added_song)
    print("--------------------------------------")
    # for index, track in enumerate(added_song):
        # print(f"{index+1}- {track}")

    # get playlist name from user and create playlist
    playlist_name = playlist_name.rsplit('/', 1)[-1]
    playlist_name = playlist_name[ 0 : 22 ]
    # print(playlist_name)
    
    # populate playlist with recommended tracks
    spotify_client.populate_playlist(playlist_name, added_song)
    # print(
    #     f"\nSong added to the playlist.")


if __name__ == "__main__":
    main()
