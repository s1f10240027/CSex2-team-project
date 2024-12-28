# pip install spotipy --upgrade が必須

import spotipy
from django.shortcuts import render
from spotipy.oauth2 import SpotifyClientCredentials

# from .music import musics, genres

# Spotifyからのデータ取得 - Privateのため.env等での非表示は省略
client_id = null
client_secret = null
auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(auth_manager=auth_manager)
# ================


def index(request):
    return render(request, "musiq/index.html")


def select_genre(request):
    return render(request, "musiq/select_genre.html")


def ranking(request):
    return render(request, "musiq/ranking.html")


def rules(request):
    return render(request, "musiq/rules.html")


def CheckSpotify(request):
    result_data = None
    form_data = {"title": "", "artist": ""}
    NotFound = None

    if request.method == "POST":
        form_data["title"] = request.POST.get("title")
        form_data["artist"] = request.POST.get("artist")
        query = f"track:{form_data["title"]}"
        if form_data["artist"]:
            query += f" artist:{form_data["artist"]}"

        try:
            result = sp.search(q=query, type="track", limit=1)
            items = result["tracks"]["items"]

            if items:
                track = items[0]
                result_data = {
                    "title": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album_image": track["album"]["images"][0]["url"],
                }
            else:
                NotFound = {"message": "曲が見つかりませんでした。"}
        except:
            NotFound = {"message": "曲が見つかりませんでした。"}

    return render(
        request,
        "musiq/CheckSpotify.html",
        {"result_data": result_data, "form_data": form_data, "NotFound": NotFound},
    )
