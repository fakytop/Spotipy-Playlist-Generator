def add_albums(albums,items):
    for item in items:
        album = {
            "id":item["id"],
            "uri":item["uri"],
            "album_name":item["name"],
            "album_type":item["album_type"],
            "total_tracks":item["total_tracks"],
            "release_date":item["release_date"],
            "release_prec":item["release_date_precision"],
            "artist_id":item["artists"][0]["id"],
            "artist_name":item["artists"][0]["name"]
        }
        print(f"💿 Album: [{album["artist_name"]}]: {album["release_date"]} - {album["album_name"]}.")
        albums.append(album)

def get_all_albums_from_artist(artist,sp):
    print(f"🔎 [{artist["artist_name"]}] Buscando discografía...")
    offset = 0
    total_albums = 0
    albums = []
    while (offset == 0 and total_albums == 0) or offset < total_albums:
        response = sp.artist_albums(artist_id = artist["artist_id"],include_groups="album,single",country="UY",offset=offset,limit=50)
        if total_albums == 0:
            total_albums = response["total"]
            print(f"ℹ️ Total de albums encontrados: {total_albums}")
        
        elements = len(response["items"])
        offset = response["offset"] + elements
        add_albums(albums,response["items"])
    return albums