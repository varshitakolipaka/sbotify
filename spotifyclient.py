import json

import requests

from track import Track
from playlist import Playlist


class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, authorization_token, user_id):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self._authorization_token = authorization_token
        self._user_id = user_id

    def get_track_recommendations(self, query):
        url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1&offset=0"
        response = self._place_get_api_request(url)
        response_json = response.json()
        # tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
        #           track in response_json["tracks"]]
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
                  track in response_json["tracks"]["items"]]
        return tracks

    def create_playlist(self, name):
        """
        :param name (str): New playlist name
        :return playlist (Playlist): Newly created playlist
        """
        data = json.dumps({
            "name": name,
            "description": "Recommended songs",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self._user_id}/playlists"
        response = self._place_post_api_request(url, data)
        response_json = response.json()

        # create playlist
        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

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

    def populate_playlist(self, playlist, tracks):
        """Add tracks to a playlist.

        :param playlist (Playlist): Playlist to which to add tracks
        :param tracks (list of Track): Tracks to be added to playlist
        :return response: API response
        """
        track_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
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
