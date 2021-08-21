import requests
from requests.models import Response

def _place_get_api_request(url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {authorization_token}"
            }
        )
        return response
playlist_id = "08TuYK3lzT0oihbi2AOPJg"
authorization_token = "BQAMrDRIp8wL544ZhQ467DjSDAR9msgoYJs9pE0Q_F1u9B7t5hyqVBZb37K1NBAsr2uNzDjFYgERHSeCeLbnLbo3eVda2Vfnej0E2h-7hSHPDbeqvlVep8PhWUZghvitPcMcOxw5RJIHXNzmPTelrbbxyBAsRskzJgBJpjRV6ELqaiVvXjZFMmoHC9EfoqaF7DaiqJ6pehXxM066c4b-mGEGjYjopvILwBTXTsPVtybanHwWhSu_tkT5DTWR0zOxMYBU-l9MggZdAJMtlZOOC0akOuvklh6G31E3HBD8"
url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
response = _place_get_api_request(url)
response_json = response.json()
num = response_json["total"]
for i in range(num):
    # print(i)
   song_name =  print(response_json["items"][i]["track"]["name"])
   song_name =  print(response_json["items"][i]["track"]["artists"]["name"])