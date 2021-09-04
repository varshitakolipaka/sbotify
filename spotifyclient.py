import json
import requests
from requests.models import Response
from track import Track
from playlist import Playlist
import validators


class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, authorization_token, user_id):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self._authorization_token = authorization_token
        self._user_id = user_id

    def get_track(self, query):
        url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1&offset=0"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
                  track in response_json["tracks"]["items"]]
        return tracks

    def check_valid_url(self, link):
        link = link.rsplit('/', 1)[-1]
        link = link[0: 22]
        url = f"https://api.spotify.com/v1/tracks/{link}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        key = 'error'
        if(key in response_json.keys()):
            return 0
        else:
            return 1

    def add_url_to_playlist(self, url, playlist_id):
        url = url.rsplit('/', 1)[-1]
        url = url[0: 22]
        url = ("spotify:track:"+url)
        list = []
        list.append(url)
        data = json.dumps(list)
        print(data)
        req_link = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = self._place_post_api_request(req_link, data)
        response_json = response.json()
        return response_json

    def create_playlist(self, name):
        """
        :param name (str): New playlist name
        :return playlist (Playlist): Newly created playlist
        """
        data = json.dumps({
            "name": name,
            "description": "Your playlist",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self._user_id}/playlists"
        response = self._place_post_api_request(url, data)
        response_json = response.json()

        # create playlist
        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def populate_playlist(self, playlist, tracks):
        """Add tracks to a playlist.

        :param playlist (Playlist): Playlist to which to add tracks
        :param tracks (list of Track): Tracks to be added to playlist
        :return response: API response
        """

        track_uris = [track.create_spotify_uri() for track in tracks]
        print(track_uris)
        data = json.dumps(track_uris)

        print(data)
        url = f"https://api.spotify.com/v1/playlists/{playlist}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        return response_json

    def delete_song_by_position(self, number, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        print(url)
        response = self._place_get_api_request(url)
        response_json = response.json()
        # tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
        #           track in response_json["tracks"]]
        track = str(response_json["items"][number-1]["track"]["id"])
        id = "spotify:track:"+track
        print(id)
        data = json.dumps({
            "tracks": [
                {
                    "uri": id
                }
            ]
        })
        print(data)
        response = self._place_delete_api_request(url, data)
        response_json = response.json()
        return response_json

    def get_total_songs(self, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = self._place_get_api_request(url)
        response_json = response.json()
        print(response_json)
        try:
            return int(response_json["total"])
        except:
            return None

    def is_song_repeat(self, playlist_id, id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = self._place_get_api_request(url)
        response_json = response.json()
        num = int(response_json["total"])
        try:
            for i in response_json["items"]:
                song_id = i["track"]["id"]
                if(song_id == id):
                    return 1
                else:
                    continue
            return None
        except:
            return None

    def rename_playlist(self, playlist_id, new_name):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        print(url)
        data = json.dumps({
            "name": new_name,
        })
        response = self._place_put_api_request(url, data)
        respnse_json = response.json()
        return respnse_json

    def describe_playlist(self, playlist_id, new_name):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        print(url)
        data = json.dumps({
            "description": new_name,
        })
        response = self._place_put_api_request(url, data)
        respnse_json = response.json()
        return respnse_json

    def populate_playlist(self, playlist, tracks):
        """Add tracks to a playlist.

        :param playlist (Playlist): Playlist to which to add tracks
        :param tracks (list of Track): Tracks to be added to playlist
        :return response: API response
        """
        track_uris = [track.create_spotify_uri() for track in tracks]
        print(track_uris)

        data = json.dumps(track_uris)
        print(data)
        url = f"https://api.spotify.com/v1/playlists/{playlist}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        return response_json

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def _place_put_api_request(self, url, data):
        response = requests.put(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def _place_delete_api_request(self, url, data):
        response = requests.delete(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def help_helper(self,prefix):
        return f'''
    All commands are preceded by a `{prefix}`. In the following commands, if set prefix is different, replace `{prefix}` by that prefix.
  - `{prefix}help` to view help regarding the commands
  
  - `{prefix}join` to join the userbase. This is required the first time you use the bot. 
  
  - `{prefix}set <playlist name>` to set current playlist to `<playlist name>`. You will be prompted to add <playlist name> if it doesn't exist.
  
  - `{prefix}show` displays the set playlist.
  
  - `{prefix}add <song name>` to add a song to the set playlist. 

  - `{prefix}delete <song_position>` to delete song at specified numeric position. 

  - `{prefix}delete last` to delete the last added song.
  
  - `{prefix}list` to list your playlists
  
  - `{prefix}list @<username>` to list <username>'s playlists. 
  
  - `{prefix}list<number>` to list playlists on page number <number>.
  
  - `{prefix}rename <new_name>` to rename the set playlist to <new_name>
  
  - `{prefix}describe` to add a description to the set playlist to the specified description.
  
  - `{prefix}lock` to lock the set playlist, so nobody except you can modify the playlist
  
  - `{prefix}unlock` to unlock the set playlist, so anyone who knows the playlist name can modify it.
  
  - `{prefix}private` to hide the set playlist, only you can view it in the `{prefix}list @<your_username>` command
  
  - `{prefix}public` to make the set playlist visible to everyone on `{prefix}list @<your_username>`

    '''
