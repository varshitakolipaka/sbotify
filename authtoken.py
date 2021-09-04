from time import time, sleep
import requests
import os
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = '''user-read-private user-read-email user-read-playback-position playlist-read-private user-library-read user-library-modify user-top-read playlist-read-collaborative playlist-modify-public playlist-modify-private ugc-image-upload user-follow-read user-follow-modify user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played'''
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
REQUEST = "https://accounts.spotify.com/api/token"
# print(CLIENT_ID)
# print(CLIENT_SECRET)
# print(REFRESH_TOKEN)
data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "refresh_token",
    "refresh_token": REFRESH_TOKEN,
    'scopes': SCOPE
}


def get_access_token():
    try:
        response = requests.post(REQUEST, data=data)
        # f = open("authtoken.txt", "a")
        # f.write(response.text)
        # f.close()
        access_token = response.json()["access_token"]
    except:
        access_token = None

    print(access_token)
    return access_token
if __name__ == "__main__":
    pass