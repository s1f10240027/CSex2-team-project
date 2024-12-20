#pip install spotipy --upgrade が必須

import random
import spotipy
from musiq.models import GameSession
from django.shortcuts import render, redirect
from spotipy.oauth2 import SpotifyClientCredentials

from .music import musics, genres

#Spotifyからのデータ取得 (動作停止済)
client_id = null
client_secret = null
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)
#================


def index(request):
    return render(request, "musiq/index.html")

def select_genre(request):
    if "session_id" in request.session:
        print("既存のIDは", request.session["session_id"], "です")
        try:
            previous = GameSession.objects.get(session_id = request.session["session_id"])
            previous.delete()
            print("GameSession が削除されました")
        except:
            print("該当のGameSessionは見つかりませんでした")
        del request.session["session_id"]
        request.session.save() 
        print("既存のsessionIDを削除しました")
    else:
        print("既存のsessionIDは存在しません")
    return render(request, "musiq/select_genre.html", {"genre": genres})

def game(request, value):
    
    if ("session_id" not in request.session) or (request.session["session_id"] == None):
        session_id = random.randint(1000,9999)
        request.session["session_id"] = session_id

        GameSession.objects.create(
            session_id = session_id,
            current_question = 1,
            correct = 0,
            answer_times = [],
            max_streak = 0,
            streak= 0,
            genre = value
        )
        print("データを作成")
    else:
        print("既存のsessoinid", request.session["session_id"])
    genreNum = 0
    matched_song = []
    for i, v in genres.items():
        if v == value:
            genreNum = i
            break
    if genreNum == 0:
        matched_song = musics.copy()
    else:
        for i in musics:
            if i[2] == genreNum:
                matched_song.append(i)
    if len(matched_song) < 4:
        print("[ERROR] ジャンルに対する楽曲数が不足しているため、Allの表示を行います")
        return redirect(game, genres[0])
    options = [None] * 4
    correct_music = random.choice(matched_song)
    index_list = [0,1,2,3]
    option_number = random.choice(index_list)
    options[option_number] = correct_music[0]
    index_list.remove(option_number)
    matched_song.remove(correct_music)
    while len(index_list) != 0:
        option_number = random.choice(index_list)
        incorrect_music = random.choice(matched_song)
        options[option_number] = incorrect_music[0]
        index_list.remove(option_number)
        matched_song.remove(incorrect_music)

    # 曲名とアーティスト名(任意)でデータ取得
    query = f"track:{correct_music[0]}"
    if correct_music[1]:
        query += f" artist:{correct_music[1]}"
    result = sp.search(q=query, type="track", limit=1)
    track = result['tracks']['items'][0]
    track_title = track['name']
    artist_name = track['artists'][0]['name']  
    album_image_url = track['album']['images'][0]['url']
    context = {
        "title": track_title,
        "artist": artist_name,
        "image": album_image_url,
        "options": {i+1: option for i, option in enumerate(options)},
        "genre": value
    }
    print(context)
    return render(request, 'musiq/game.html', context)

def CalcScore(correct,consecutive,avetime):
    if correct == 0:
        return 0
    score = 0

    #正解処理
    score += (correct * 16)

    #連続ボーナス
    score += (consecutive * 2)

    #平均回答時間
    if avetime >= 8000:
        score += 0
    elif avetime <= 1500:
        score += 10
    else:
        score += (11.5 - (avetime/1000))

    return score


def Ingame_savedata(request):
    if request.method == "POST":
        isCorrect = int(request.POST.get("isCorrect"))
        answer_time = int(request.POST.get("answer_time"))
        print(request.POST)

        id = request.session.get("session_id")
        gamedata = GameSession.objects.get(session_id = id)
        gamedata.answer_times.append(answer_time)
        
        if isCorrect == True:
            gamedata.correct += 1
            gamedata.streak += 1
            if gamedata.streak > gamedata.max_streak:
                gamedata.max_streak = gamedata.streak
        else:
            gamedata.streak = 0
        
        if gamedata.current_question == 5:
            print(f"id: {gamedata.session_id}, \ncorrect: {gamedata.correct}, \ntime: {gamedata.answer_times}, \nstreak: {gamedata.streak}, \nmax: {gamedata.max_streak}")
            Score = CalcScore(
                gamedata.correct, 
                gamedata.max_streak, 
                sum(gamedata.answer_times) / len(gamedata.answer_times)
            )
            print(f"あなたのスコアは... {Score} でしたー！！！")
            gamedata.delete()
            return redirect(index)
        else:
            gamedata.current_question += 1

        gamedata.save()
        return redirect(game, gamedata.genre)
    else:
        return redirect(index)

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
            items = result['tracks']['items']

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

    return render(request, "musiq/CheckSpotify.html", {"result_data": result_data, "form_data": form_data, "NotFound": NotFound})   

def ranking(request):
    return render(request, "musiq/ranking.html")

def rules(request):
    return render(request, "musiq/rules.html")