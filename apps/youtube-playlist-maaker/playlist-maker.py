import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# OAuth 2.0 scopes for the YouTube API
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Path to your client_id.json
CLIENT_SECRETS_FILE = "client_id.json"

# Function to authenticate using OAuth 2.0 and return the YouTube API service
def get_authenticated_service():
    # Create the flow using the client secrets file and the scopes
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    
    # Specify the redirect URI (make sure it matches the one in your credentials)
    flow.redirect_uri = 'http://localhost:64430/'
    
    # Request access type "offline" for refresh token, and response_type "code"
    flow.access_type = 'offline'
    flow.response_type = 'code'

    # Run the OAuth flow and obtain the credentials
    credentials = flow.run_local_server(port=64430)

    # Build and return the YouTube API client
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube

# Example of creating a YouTube playlist
def create_playlist(youtube, title, description):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    response = request.execute()
    print(f"Playlist created: {response['snippet']['title']}")
    return response

if __name__ == '__main__':
    # Authenticate and get the YouTube service
    youtube = get_authenticated_service()

    # Create a playlist
    title = "My New Playlist"
    description = "This is a test playlist created via OAuth2 in Python"
    create_playlist(youtube, title, description)
