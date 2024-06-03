import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

# User credentials and details
username = "cwwn8oq4zxjcm81ny63fwr9mk"
client_id = "3a97225143084aefb89a00c20dd43547"
client_secret = "1013b6c189684248b842c82ca1e0b152"
redirect_uri = "http://google.com/callback/"

def authenticate_spotify(client_id, client_secret, redirect_uri):
    try:
        scope = "user-read-playback-state,user-modify-playback-state"
        oauth_object = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
        token_dict = oauth_object.get_access_token()
        token = token_dict['access_token']
        spotify_object = spotipy.Spotify(auth=token)
        user_name = spotify_object.current_user()
        return spotify_object, user_name
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return None, None

def open_playlist_by_mood(client_id, client_secret, redirect_uri, mood):
    try:
        spotify_object, user_name = authenticate_spotify(client_id, client_secret, redirect_uri)
        if not spotify_object or not user_name:
            print("Authentication failed.")
            return

        print(f"Welcome, {user_name['display_name']}")

        results = spotify_object.search(mood + " playlist", 1, 0, "playlist")
        playlists_dict = results['playlists']
        playlist_items = playlists_dict['items']
        if playlist_items:
            playlist_uri = playlist_items[0]['uri']
            playlist_url = playlist_items[0]['external_urls']['spotify']

            # Open the playlist in the web browser
            webbrowser.open(playlist_url)
            print('Playlist has opened in your browser.')

            # Get the user's devices
            devices = spotify_object.devices()
            if devices['devices']:
                device_id = devices['devices'][0]['id']
                spotify_object.start_playback(device_id=device_id, context_uri=playlist_uri)
                print('Playlist is now playing.')
            else:
                print("No active devices found. Please open Spotify on a device and try again.")
        else:
            print("No playlists found with that mood.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
mood = input("Enter the mood for the playlist: ")
open_playlist_by_mood(client_id, client_secret, redirect_uri, mood)
