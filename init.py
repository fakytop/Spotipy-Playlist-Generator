import spotipy
from save_files import save_json_file,save_xlsx_file
from albums_manager import get_all_albums_from_artist
from tracks_manager import get_tracks_id_from_albums,get_tracks_info,calculate_score,get_the_firsts_ids
from artists_manager import save_artist_popularity,read_file_to_list_of_dicts,get_artists_info,save_artists_data
from spotipy.oauth2 import SpotifyOAuth
import json
import os
from dotenv import load_dotenv

load_dotenv()
artists = read_file_to_list_of_dicts("artists.xlsx",file_type="excel")
print("\n🚀 Iniciando proceso...")
print(f"\n📂 {len(artists)} artistas cargados desde el archivo.")

CLIENT_ID = os.getenv("CLIENT_ID")
SECRET_ID = os.getenv("SECRET_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

SCOPE = "playlist-modify-public playlist-modify-private"

def get_spotify_customer():
    auth_manager = SpotifyOAuth(client_id=CLIENT_ID,
                                client_secret=SECRET_ID,
                                redirect_uri=REDIRECT_URI,
                                scope=SCOPE,
                                open_browser=True
    )
    
    return spotipy.Spotify(auth_manager=auth_manager)

sp = get_spotify_customer()

artists = get_artists_info(sp,artists)
artists = save_artists_data(artists)
save_json_file(artists,"generated_files/artists_info.json")
save_xlsx_file(artists,"generated_files/artists_info.xlsx")
albums = []

print("\n--- PASO 1: Recopilando álbumes ---")
for artist in artists:
    artist_albums = get_all_albums_from_artist(artist,sp)
    albums.extend(artist_albums)
    # get_albums_from_artist(artist["artist_id"],albums,sp)
    # save_artist_popularity(artist,sp)

print("\n--- PASO 2: Recopilando tracks ---")
tracks_id = get_tracks_id_from_albums(albums,sp,548)

print("\n--- PASO 3: Obteniendo info de tracks ---")
tracks_info = get_tracks_info(tracks_id,sp)

print("\n--- PASO 4: Calculando scores ---")
calculate_score(tracks_info,artists,0.45,0.0020,0.35,0.5)

tracks_info = sorted(tracks_info,key= lambda track: track["score"],reverse=True)

save_xlsx_file(tracks_info,"generated_files/tracks_metadata.xlsx")
save_xlsx_file(artists,"generated_files/artists_metadata.xlsx")


tracks_id = get_the_firsts_ids(tracks_info,200)
print(f"\n--- PASO 5: Actualizando playlist con los top {len(tracks_id)} tracks ---")
sp.playlist_replace_items("05Wc2fcgTMJSOqWIniDV7p",tracks_id[:100])
sp.playlist_add_items("05Wc2fcgTMJSOqWIniDV7p",tracks_id[100:200])
print(f"✔️ Proceso finalizado con éxito.")