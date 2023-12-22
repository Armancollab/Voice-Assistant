import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import os
import subprocess

# Spotify API authentication
client_id = 'e33c34695b8c4c6d9dc9b7bfafc17a69'
client_secret = 'da66153fd27b4224a46dfa16c4ce038b'
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Track information
track_name = 'Shape of You'

# Search for the track
results = sp.search(q=track_name, limit=1)

# Download track if found
if results['tracks']['items']:
    track = results['tracks']['items'][0]
    if track['preview_url']:
        preview_url = track['preview_url']
        print(
            f"Downloading '{track['name']}' by {', '.join([artist['name'] for artist in track['artists']])}")

        # Download the track
        response = requests.get(preview_url)
        # Specify the desired local file path
        audio_file_path = f'{track_name}.mp3'
        with open(audio_file_path, 'wb') as f:
            f.write(response.content)

        # Launch the default music player to play the downloaded song
        os.startfile(audio_file_path)
    else:
        print(f"No preview available for '{track_name}'")
else:
    print(f"No track found for '{track_name}'")
