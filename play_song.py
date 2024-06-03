import json 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

username = "cwwn8oq4zxjcm81ny63fwr9mk"
client_id = "3a97225143084aefb89a00c20dd43547"
client_secret = "1013b6c189684248b842c82ca1e0b152"
redirect_uri = "http://google.com/callback/"



def authenticate_spotify(client_id, client_secret, redirect_uri):
    try:
        oauth_object = SpotifyOAuth(client_id, client_secret, redirect_uri)
        token_dict = oauth_object.get_access_token()
        token = token_dict['access_token']
        spotify_object = spotipy.Spotify(auth=token)
        user_name = spotify_object.current_user()
        return spotify_object, user_name
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return None, None

#to print the response in readable format
#print(json.dumps(user_name, sort_keys=True, indent=4))

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
            playlist = playlist_items[0]['external_urls']['spotify']
            webbrowser.open(playlist)
            print('Playlist has opened in your browser.')
        else:
            print("No playlists found with that mood.")
    except Exception as e:
        print(f"An error occurred: {e}")

#example usage
#mood = input("Enter the mood for the playlist: ")
#open_playlist_by_mood(client_id, client_secret, redirect_uri, mood)