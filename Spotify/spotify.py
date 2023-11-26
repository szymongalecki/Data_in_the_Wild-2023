import json
import spotipy
import datetime
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import CLIENT_ID, CLIENT_SECRET


"""
Connection to Spotify API
"""
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
)

"""
Playlists for Polish Rap music
"""
rap_generacja = (
    "https://open.spotify.com/playlist/37i9dQZF1DWXJnyndhASBe?si=758917be953a4ebd"
)
polski_hip_hop_klasyki = (
    "https://open.spotify.com/playlist/37i9dQZF1DX6pGi5vfd9k8?si=a74e8cccf8ec49e7"
)
polski_rap_2000 = (
    "https://open.spotify.com/playlist/37i9dQZF1DX4tIiLXPvlZC?si=5a204cefe1ac45ab"
)
polski_rap_2010 = (
    "https://open.spotify.com/playlist/37i9dQZF1DX2htXmbzwcfL?si=8c8cb30c01f3448a"
)

"""
Playlists for Croatian Rap music
"""
this_is_tram_11 = (
    "https://open.spotify.com/playlist/37i9dQZF1DZ06evO4ecEOC?si=f9f19d3ff1de4475"
)
bolesna_braca = (
    "https://open.spotify.com/playlist/37i9dQZF1E4mRVwtHBO6wH?si=7b8aa1cf887f4841"
)
marin_ivanovic_stoka = (
    "https://open.spotify.com/playlist/37i9dQZF1E4whjB3IyUubA?si=555d49ce9e644af6"
)
kid_rada = (
    "https://open.spotify.com/playlist/37i9dQZF1E4xQZ3DjXINt5?si=447a5dfdec2c495d"
)


def playlist(url: str) -> dict:
    """
    Returns a playlist dictionary given a spotify url
    """
    playlist = spotify.playlist_items(url)
    return playlist


def playlist_name(url: str) -> str:
    """
    Returns playlist name given a spotify url
    """
    playlist = spotify.playlist(url)
    return playlist["name"].strip().lower().replace(" ", "_")


def songs_and_artists(path: str) -> dict:
    """
    Returns a dictionary with song names and artists from a playlist json file
    """
    name_artists = []
    with open(path) as f:
        results = json.load(f)
    songs = results["items"]
    for song in songs:
        artists = [artist["name"] for artist in song["track"]["artists"]]
        name = song["track"]["name"]
        print(f"{name} - {artists}")
        name_artists.append({"name": name, "artists": artists})
    songs_and_artists = {"items": name_artists}
    return songs_and_artists


def save_to_json(name: str, content: dict, directory: str) -> str:
    """
    Saves dictionary to a json file at given directory
    """
    date = datetime.datetime.now().strftime("%d-%m-%y")
    path = f"{directory}/{name}_{date}.json"
    with open(path, "w") as f:
        json.dump(content, f, indent=4)
    return path


def save_playlist_and_songs(url: str) -> None:
    """
    Saves playlist and songs from a given url to json files
    """
    path_to_playlists = save_to_json(
        name=playlist_name(url), content=playlist(url), directory="playlists"
    )
    save_to_json(
        name=playlist_name(url),
        content=songs_and_artists(path_to_playlists),
        directory="songs",
    )


def albums(artist_id: str) -> dict:
    """
    Returns a dictionary with album name and album id from a given artist id
    """
    albums = spotify.artist_albums(artist_id)
    return [
        {"name": album["name"], "id": album["id"]}
        for album in albums["items"]
        if album["album_type"] == "album"
    ]
