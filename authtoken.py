from time import time, sleep

CLIENT_ID = "468cc00d10c643708ce19aa7d7203b8d"
CLIENT_SECRET = "79f9cadb0c3941a6b3ed08617c1e69ec"
SCOPE = ["user-read-private", "user-read-email"]
REFRESH_TOKEN = "AQDTm59BeNkNUdj1khLih3cuzL4BvMbz8V2b4Eic4AnwFpMPzybyTwgO-QP8-IuOmg6FvPanpWiDm1wN4CyLfFBoSe50Z4s405xf-gRDd985FLky-5G53iLEnchpsXCDbY4"
REQUEST = "https://accounts.spotify.com/api/token"

data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "refresh_token",
    "refresh_token": REFRESH_TOKEN,
    "scopes": SCOPE,
}

while True:
    import requests

    try:
        response = requests.post(REQUEST, data=data)
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
