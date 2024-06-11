import requests
from requests_oauthlib import OAuth2Session

from consts import TOKEN_URL


class TiktokAdapter:
    def __init__(self, client_key: str, client_secret: str, refresh_token: str, access_token: str = None):
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token

    def upload_video(self, access_token, video_path, description):
        if not self.check_access_token_validity():
            self.refresh_access_token()

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        files = {
            'video': open(video_path, 'rb'),
            'description': (None, description)
        }
        response = requests.post('https://open-api.tiktok.com/video/upload/', headers=headers, files=files)
        return response.json()

    def refresh_access_token(self):
        extra = {
            'client_id': self.client_key,
            'client_secret': self.client_secret
        }
        oauth = OAuth2Session(self.client_key, token={
            'refresh_token': self.refresh_token,
            'token_type': 'Bearer',
            'expires_in': -30  # Expired token
        })
        new_token = oauth.refresh_token(TOKEN_URL, **extra)
        self.access_token = new_token

    def check_access_token_validity(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = requests.get('https://open-api.tiktok.com/user/', headers=headers)

        if response.status_code == 200:
            print("Access token is valid.")
            return True
        elif response.status_code == 401:
            print("Access token is invalid or expired.")
            return False
        else:
            print(f"Failed to check access token validity. Status code: {response.status_code}")
            return False
