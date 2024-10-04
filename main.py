from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
load_dotenv("C:/Python/Environmental variables/.env")

user_id = "31lrqcpexwl6uwnosjxcijd7wkaa"
spotify_client_id = os.getenv("spotify_client_id")
spotify_client_secret = os.getenv("spotify_client_secret")
redirect_url = os.getenv("redirect_url")
date = input("Type the date in this format YYYY-MM-DD: ")
BILLBOARD_URL = f"https://www.billboard.com/charts/hot-100/{date}/"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                       client_secret=spotify_client_secret,
                                                       redirect_uri=redirect_url,
                                                       scope="playlist-modify-private",
                                                       cache_path="token.txt"))

client_credentials_manager = SpotifyClientCredentials(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret
        )
sp_search = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}
response = requests.get(BILLBOARD_URL, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
top_songs = soup.select("h3.c-title.a-no-trucate")
top_artists = soup.select("span.c-label.a-no-trucate")
top_100_songs = []
all_artists = []
for song in top_songs:
    title = song.get_text().strip()
    top_100_songs.append(title)

for artist in top_artists:
    name = artist.get_text().strip()
    all_artists.append(name)

song_artist_dict = {top_100_songs[i]: all_artists[i] for i in range(len(top_100_songs))}

all_songs_uri = []
for (song_name,artist) in song_artist_dict.items():
    for symbol in ["Featuring", "&", "x", "X", "("]:
        if symbol in artist:
            artist = artist.split(symbol)[0]
    results = sp_search.search(q=f'track: {song_name} artist: {artist}',type='track',limit=1,offset=0)
    try:
        song_uri= results["tracks"]["items"][0]["uri"]
        all_songs_uri.append(song_uri)
    except IndexError:
        print(f"no song found on this title - {song_name}")
print(all_songs_uri)
# playlist_name = "BillBoard Playlist"
# playlist_description = "A playlist created with Spotipy using BillBoard Scarping!"
# playlist = sp.user_playlist_create(user=user_id,
#                                    name=playlist_name,
#                                    public=False,
#                                    description=playlist_description)

# print(f"Created Playlist: {playlist['name']} with id: {playlist['id']}")
playlist_id = "2UdBAtOnbUuMQnOxCNLVXj"
add_track = sp.playlist_add_items(playlist_id=playlist_id,items=all_songs_uri)