from datetime import date, timedelta,datetime
import math

def save_artists_info(artists):
    artists_info = []
    for artist in artists:
        artist_info = {
            "id":artist["id"],
            "uri":artist["uri"],
            "name":artist["name"],
            "type":artist["type"]
        }
        artists_info.append(artist_info)
    return artists_info

def show_artists_names(artists):
    artists_names = []
    for artist in artists:
        artists_names.append(artist["name"])
    return artists_names

def exists_id_in_array(tracks_id, track_id):
    for id in tracks_id:
        if id == track_id:
            return True
    return False

def save_tracks_id_from_albums(album,sp):
    tracks_id = []
    album_tracks = sp.album_tracks(album["id"])
    for track in album_tracks["items"]:
        if not exists_id_in_array(tracks_id,track["id"]):
            tracks_id.append(track["id"])
    return tracks_id

def read_albums_to_save_tracks_id(albums,limit_date,sp):
    seen = set()
    tracks_id = []
    for album in albums:
        release_prec = album["release_prec"]
        if release_prec == "day":
            release_date = datetime.strptime(album["release_date"],"%Y-%m-%d").date()
        else:
            release_date = datetime.strptime(album["release_date"],"%Y").date()
        if release_date >= limit_date:
            for track_id in save_tracks_id_from_albums(album,sp):
                if track_id not in seen:
                    seen.add(track_id)
                    tracks_id.append(track_id)
    print(f"   🎵 {len(tracks_id)} tracks únicos recolectados hasta ahora.")
    return tracks_id

def get_tracks_id_from_albums(albums,sp,diff_days):
    limit_date = date.today() - timedelta(days=diff_days)
    print(f"\n📅 Filtrando tracks lanzados después del {limit_date}...")
    tracks_id = read_albums_to_save_tracks_id(albums,limit_date,sp)
    return tracks_id

def save_tracks_info(tracks_info,response):
    tracks = response["tracks"]
    for track in tracks:
        track_info = {
            "id": track["id"],
            "uri": track["uri"],
            "href": track["href"],
            "name": track["name"],
            "artists": save_artists_info(track["artists"]),
            "album_album_type": track["album"]["album_type"],
            "album_type": track["album"]["type"],
            "album_name": track["album"]["name"],
            "album_release_date": track["album"]["release_date"],
            "album_release_prec": track["album"]["release_date_precision"],
            "popularity": track["popularity"]
        }
        tracks_info.append(track_info)
        print(f"   📦 Lote procesado: {len(tracks_info)} tracks en total hasta ahora.")

def save_response_tracks(ask_tracks_ids,tracks_info,sp):
    response = sp.tracks(ask_tracks_ids)
    save_tracks_info(tracks_info,response)
    ask_tracks_ids.clear()

def get_tracks_info(tracks_id,sp):
    ask_tracks_ids = []
    tracks_info = []
    
    for id in tracks_id:
        ask_tracks_ids.append(id)
        if len(ask_tracks_ids) == 50:
            save_response_tracks(ask_tracks_ids,tracks_info,sp)
    if len(ask_tracks_ids) > 0:
        save_response_tracks(ask_tracks_ids,tracks_info,sp)
    return tracks_info

#boost se define como 0.8 x default
#lambd se define como 0.0025 x default
def multiplier_time(diff_days,boost,lambd):
    if diff_days <= 30:
        return 1 + boost * ((30 - diff_days)/30)
    if  diff_days > 30 and diff_days <= 90:
        return 1
    return math.exp(-lambd*(diff_days-90))

def multiplier_artist(pop_artist,weight):
    return 1 + pop_artist / 100 * weight

def bonus_artist(powerBonus,pop_artist,diff_days):
    return 1 + powerBonus * (1 - pop_artist/100) * max(0,(14-diff_days)/14)

def get_artist_pop(artists,artist):
    for art in artists:
        if art["artist_id"] == artist["id"]:
            return art["popularity"]
    return 0

def get_average_pop_artists(artists,artistsSong):
    qant = 0
    sumPop = 0
    for artist in artistsSong:
        pop = get_artist_pop(artists,artist)
        if pop > 0:
            qant += 1
            sumPop += pop
    if qant > 0:
        return sumPop / qant
    else:
        return 0

def calculate_score(tracks_info,artists,boost,decay_rate,weight_art,pwr_bonus):
    for track in tracks_info:
        avg_pop_artist = get_average_pop_artists(artists,track["artists"])
        if track["album_release_prec"] == "day":
            release_date = datetime.strptime(track["album_release_date"],"%Y-%m-%d").date()
        else:
            release_date = datetime.strptime(track["album_release_date"],"%Y").date()
        diff_days = (date.today() - release_date).days
        score = track["popularity"] * multiplier_time(diff_days,boost,decay_rate) * multiplier_artist(avg_pop_artist,weight_art) * bonus_artist(pwr_bonus,avg_pop_artist,diff_days)
        track["score"] = score
        print(f"   🎵 {track['name'][:40]:<40} score: {score:.2f}  (hace {diff_days}d, pop. artista: {avg_pop_artist:.0f})")

def get_the_firsts_ids(track_list, count):
    if len(track_list) < count:
        count = len(track_list)
    return [track["id"] for track in track_list[:count]]
