from time import time, sleep

CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
SCOPE = '''user-read-private user-read-email user-read-playback-position playlist-read-private user-library-read user-library-modify user-top-read playlist-read-collaborative playlist-modify-public playlist-modify-private ugc-image-upload user-follow-read user-follow-modify user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played'''
REFRESH_TOKEN = "refresh_token"
REQUEST = "https://accounts.spotify.com/api/token"

data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "refresh_token",
    "refresh_token": REFRESH_TOKEN,
    'scopes': SCOPE
}
f = open("authtoken.txt", "w")
f.write(str(data))
f.write("\n====================================\n")
f.close()
while True:
    import requests

    try:
        response = requests.post(REQUEST, data=data)
        f = open("authtoken.txt", "a")
        f.write(response.text)
        f.close()
        access_token = response.json()["access_token"]
    except:
        access_token = None

    # print(access_token)
    sleep(3599 - time() % 3599)

    f = open('.env', 'w')
    to_write = '''SPOTIFY_USER_ID="y4ob0twgc8h44hcxkor64bvc3"''' + \
        '\n'+'''SPOTIFY_AUTHORIZATION_TOKEN="'''+access_token+'"'+'\n'
    # print(to_write)
    f.write(to_write)
    f.close()
    # break
