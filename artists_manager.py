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
