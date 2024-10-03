from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
load_dotenv("C:/Python/Environmental variables/.env")

spotify_client_id = os.getenv("spotify_client_id")
spotify_client_secret = os.getenv("spotify_client_secret")
redirect_url = os.getenv("redirect_url")

date = input("Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
top_songs = soup.select("h3.c-title.a-no-trucate")
artists = soup.select("span.c-label.a-no-trucate")
all_artists = []
for artist in artists:
    name = artist.get_text().strip()
    all_artists.append(name)
print(all_artists)
modified = []
for name in all_artists:
    for symbol in ["Featuring","&","x","X","("]:
        if symbol not in name:
            modified.append(name)
        elif symbol in name:
            mod = name.split(symbol)[0]
            modified.append(mod)
            break
print(modified)
# res = {test_keys[i]: test_values[i] for i in range(len(test_keys))}
top_100_songs = []
for song in top_songs:
    title = song.get_text().strip()
    top_100_songs.append(title)
print(len(top_100_songs))

#
#
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
#                                                client_secret=spotify_client_secret,
#                                                redirect_uri=redirect_url,
#                                                scope="playlist-modify-private",
#                                                cache_path="token.txt"))
# # user = sp.current_user()
# # print(user)
# # user_id = user["id"]
# # print(user_id)
#
#
#
# song_uris = []
# year = date.split("-")[0]
# for song in top_100_songs:
#     result = sp.search(q=f"track:{song} year:{year}", type="track")
#     print(result)
#     try:
#         uri = result["tracks"]["items"][0]["uri"]
#         song_uris.append(uri)
#     except IndexError:
#         print(f"{song} doesn't exist in Spotify. Skipped.")