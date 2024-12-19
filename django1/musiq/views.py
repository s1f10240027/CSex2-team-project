#pip install spotipy --upgrade が必須

import random
from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .music import musics

#Spotifyからのデータ取得 (動作停止済)
client_id = null
client_secret = null
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)
#================


def index(request):
    return render(request, "musiq/index.html")

def select_genre(request):
    return render(request, "musiq/select_genre.html")


def game(request):
    options = [None] * 4
    music = random.choice(musics)
    index_list = [0,1,2,3]
    option_number = random.choice(index_list)
    options[option_number] = music[0]
    index_list.remove(option_number)
    while len(index_list) != 0:
        option_number = random.choice(index_list)
        i = random.randint(0, len(musics) -1)
        if musics[i][0] not in options:
            options[option_number] = musics[i][0]
            index_list.remove(option_number)

    # 曲名とアーティスト名(任意)でデータ取得
    query = f"track:{music[0]}"
    if music[1]:
        query += f" artist:{music[1]}"
    result = sp.search(q=query, type="track", limit=1)
    track = result['tracks']['items'][0]
    track_title = track['name']
    artist_name = track['artists'][0]['name']  
    album_image_url = track['album']['images'][0]['url']
    context = {
        "title": track_title,
        "artist": artist_name,
        "image": album_image_url,
        "options": {i+1: option for i, option in enumerate(options)}
    }
    print(context)
    return render(request, 'musiq/game.html', context)






def ranking(request):
    return render(request, "musiq/ranking.html")

def rules(request):
    return render(request, "musiq/rules.html")