from save_files import save_json_file
import pandas as pd
import os

def save_artist_popularity(artist,sp):
    tracks = sp.artist_top_tracks(artist["artist_id"],country="UY")
    print(f"\n👤 [{artist["artist_name"]}] Calculando popularidad promedio...")
    tracks = tracks["tracks"]
    qant = 0
    sum_popularity = 0
    for track in tracks:
        qant += 1
        sum_popularity += track["popularity"]

    artist["popularity"] = sum_popularity / qant
    print(f"   🎯 Popularidad: {artist["popularity"]:.1f}")


def read_file_to_list_of_dicts(filename, file_type='excel'):
    file_path = os.path.join(os.getcwd(),filename)
    data_list = []
    
    if not os.path.exists(file_path):
        print(f"Error: El archivo '{file_path}' no se encontró")
        return []

    df = pd.read_excel(file_path)
    
    data_list = df.to_dict(orient='records')
    
    return data_list

def get_artists_info(sp,id_artists):
    artist_id_list = []
    artists = []
    for id_artist in id_artists:
        artist_id_list.append(id_artist["artist_id"])
        if len(artist_id_list) == 50:
            artists.extend(sp.artists(artist_id_list)["artists"])
            artist_id_list.clear()
    if len(artist_id_list) > 0:
        artists.extend(sp.artists(artist_id_list)["artists"])
    return artists

def get_genres(genres):
    genres_name = ""
    total_genres = len(genres)
    counter = 0
    for genre in genres:
        genres_name += genre
        counter += 1
        if counter < total_genres:
            genres_name += ","
    return genres_name

def save_artists_data(list_artists):
    artists = []
    
    for artist in list_artists:
        art = {
            "artist_name": artist["name"],
            "artist_id": artist["id"],
            "popularity": artist["popularity"],
            "genres": get_genres(artist["genres"]),
            "followers": artist["followers"]["total"]
        }
        artists.append(art)
    return artists


