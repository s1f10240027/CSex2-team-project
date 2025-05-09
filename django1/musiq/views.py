#pip install spotipy --upgrade が必須

import re
import math
import random
import spotipy
from django.conf import settings
from musiq.models import GameSession, Account
from django.contrib import messages
from django.contrib.staticfiles import finders
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from spotipy.oauth2 import SpotifyClientCredentials
from .music import musics, genres

#Spotifyからのデータ取得 
client_id = null #既に失効済み
client_secret = null #既に失効済み
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)
#================

#ログイン画面
def login_view(request):
    if request.method == 'POST':
        if request.POST.get("from_Result", False):
            request.session["return_Result"] = True
            return render(request, "musiq/login.html", {"ReturnResult": True})
        if request.POST["name"] == "":
            print("ログインです")
            account = ""
            email_or_username = request.POST.get('email', '')
            password = request.POST.get('password', '')

            if email_or_username == "" or password == "":
                print(request, "メールアドレス/ユーザー名またはパスワードが空です。")
                return redirect('login')

            regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if re.match(regex, email_or_username):
                try:
                    account = Account.objects.get(email=email_or_username)
                    username = account.username
                except Account.DoesNotExist:
                    print(request, "メールアドレスが登録されていません。")
                    return redirect('login')
                
            else:
                try:
                    account = Account.objects.get(username=email_or_username)
                    username = account.username
                except Account.DoesNotExist:
                    print(request, "ユーザー名が登録されていません。")
                    return redirect('login')
                
            if check_password(password, account.password):
                request.session['username'] = account.username
                request.session.save()
                if request.session.get("return_Result", False):
                    return redirect(result)    
                return redirect('index')
            else:
                print(request, "パスワードが正しくありません。")
                return redirect('login')
        else:
            print("新規登録です")

            username = request.POST["name"]
            email = request.POST["email"]
            password = request.POST["password"]

            if Account.objects.filter(email=email).exists():
                print(request, "このメールアドレスは既に登録されています。")
                return render(request, 'musiq/login.html', {'username': username, 'email': email, 'password': password, 'confirm': password, 'sign_up': True})
            if Account.objects.filter(username=username).exists():
                print(request, "このユーザー名は既に使用されています。")
                return render(request, 'musiq/login.html', {'username': username, 'email': email, 'password': password, 'confirm': password, 'sign_up': True})

            hashed_password = make_password(password)
            Account.objects.create(
                username=username,
                email=email,
                password=hashed_password,
            )
            print(request, "新規登録が完了しました！")
            request.session['username'] = username
            request.session.save()
            if request.session.get("return_Result", False):
                return redirect(result)    
            return redirect('index') 
    else:
        return render(request, "musiq/login.html")


#ユーザーアイコンを取得する関数
def getUserIcon(userData):
    icon = ""
    if userData.userIcon:
        icon = userData.userIcon.url
    else:
        icon = settings.STATIC_URL + 'media/default_icon.png'
    return icon

#TOPページ
def index(request):
    deleteSession(request)
    name = request.session.get('username', None)
    userIcon = settings.STATIC_URL + 'media/nologin.png'
    shuffle1 = random.sample(range(1, 10), 9)
    shuffle2 = random.sample(range(1, 10), 9)
    if name:
        user = Account.objects.get(username=name)
        userIcon = getUserIcon(user)
        return render(request, 'musiq/index.html', {'user': user, 'userIcon': userIcon, 'shuffle': {1: shuffle1, 2: shuffle2}})
    return render(request, "musiq/index.html", {'user': None, 'userIcon': userIcon, 'shuffle': {1: shuffle1, 2: shuffle2}})

#セッションデータを消去するための関数
def deleteSession(request):
    if "session_id" in request.session:
        try:
            previous_session = GameSession.objects.get(session_id=request.session["session_id"])
            previous_session.delete()
            print("GameSession が削除されました")
        except ObjectDoesNotExist:
            print("該当のGameSessionは見つかりませんでした")
    for key in ["session_id", "matched_song", "score", "correct_music", "return_Result"]:
        if key in request.session:
            del request.session[key]
            print(f"{key}がリクエストから削除されました")
        else:
            print(f"{key}はリクエストに存在しません")
    request.session.save() 

#ジャンル選択画面
def select_genre(request):
    deleteSession(request)
    return render(request, "musiq/select_genre.html", {"genre": genres})

#リトライボタン入力時
def retry(request):
    id = request.session.get("session_id")
    value = GameSession.objects.get(session_id=id).genre
    deleteSession(request)
    return redirect(game, value)

#ゲーム画面
def game(request, value):
    if ("session_id" not in request.session) or (request.session["session_id"] == None):
        session_id = random.randint(1000,9999)

        matched_song = []
        lacksong_state = None
        genreNum = 0
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

        if len(matched_song) < 5:
            lacksong_state = True
            value = genres[0]
            matched_song.clear()
            matched_song = musics.copy()

        request.session["session_id"] = session_id
        request.session["matched_song"] = matched_song
        request.session["correct_music"] = []
        request.session.save()

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
        if lacksong_state == True:
            print("[ERROR] ジャンルに対する楽曲数が不足しているため、Allの表示を行います")
            return redirect(game, genres[0])
        else:
            print("既存のsessoinid", request.session["session_id"])

    genre_songs_list = []
    genreNum2 = 0
    for i, v in genres.items():
        if v == value:
            genreNum2 = i
            break
    if genreNum2 == 0:
        genre_songs_list = musics.copy()
    else:
        for i in musics:
            if i[2] == genreNum2:
                genre_songs_list.append(i)

    options = [None] * 4
    correct_music = random.choice(request.session["matched_song"])
    ExistState = False
    while ExistState == False:
        if finders.find("musics/" + correct_music[0] + ".mp3"):
            ExistState = True
            break
        else:
            correct_music = random.choice(request.session["matched_song"])
            print("楽曲が見つかりませんでした。再度抽選します。")
    print("正解曲:")
    print(correct_music)
    
    index_list = [0,1,2,3]
    option_number = random.choice(index_list)
    options[option_number] = correct_music[0]

    index_list.remove(option_number)
    genre_songs_list.remove(correct_music)

    request.session["matched_song"].remove(correct_music)
    request.session["correct_music"].append(correct_music[0])
    request.session.save()

    while len(index_list) != 0:
        option_number = random.choice(index_list)
        incorrect_music = random.choice(genre_songs_list)
        options[option_number] = incorrect_music[0]
        index_list.remove(option_number)
        genre_songs_list.remove(incorrect_music)
    query = f"track:{correct_music[0]}"
    if correct_music[1]:
        query += f" artist:{correct_music[1]}"
    result = sp.search(q=query, type="track", limit=1)
    track = result['tracks']['items'][0]
    artist_name = track['artists'][0]['name']  
    album_image_url = track['album']['images'][0]['url']

    context = {
        "title": correct_music[0],
        "artist": artist_name,
        "image": album_image_url,
        "options": {i+1: option for i, option in enumerate(options)},
        "genre": value,
        "current": GameSession.objects.get(session_id = request.session["session_id"]).current_question
    }

    return render(request, 'musiq/game.html', context)

#スコア計算関数
def CalcScore(correct,consecutive,avetime):
    if correct == 0:
        return 0
    score = 0

    #正解処理
    score += (correct * 16)
# - 80
    #連続ボーナス
    score += (consecutive * 2)
# - 10   
    #平均回答時間
    if avetime >= 10000: #10秒以上は+0
        pass
    elif avetime <= 2000: 
        score += 10
    else:
        score += (12 - (avetime/1000))
# - 10
# 正解数 * 16 + 連続正解数 * 2 + (12 - (平均回答時間 / 1000))
    return round(score, 2)

#リザルト画面
def result(request):
    name = request.session.get('username', None)
    score = request.session.get("score")
    user_icon = settings.STATIC_URL + 'media/nologin.png'

    high_user = {'username': None, 'userIcon': None, 'score': None, 'rank': None}
    low_user  = {'username': None, 'userIcon': None, 'score': None, 'rank': None}

    sort_by_score = Account.objects.all().order_by('-best_score')
    i = 0
    rank = 1
    for other in sort_by_score:
        if other.best_score <= score:
            break
        rank += 1
    up_rank = rank - 1
    under_rank = rank + 1
    try:
        index = rank - 2
        if sort_by_score[index].username == name:
            if sort_by_score[index].best_score == score:
                index -= 1
            else:
                high_user['username'] = "あなたの最高記録"
            
        if high_user['username'] == None:
            high_user['username'] = sort_by_score[index].username
        high_user['userIcon'] = getUserIcon(sort_by_score[index])
        high_user['score'] = sort_by_score[index].best_score
        high_user['rank'] = up_rank
    except:
        print("上位のプレイヤーが存在しません")

    try:
        index = rank - 1
        if sort_by_score[index].username == name:
            if sort_by_score[index].best_score == score:
                index += 1  
            else:
                low_user['username'] = "あなたの最高記録"
        if low_user['username'] == None:
            low_user['username'] = sort_by_score[index].username
        low_user['userIcon'] = getUserIcon(sort_by_score[index])
        low_user['score'] = sort_by_score[index].best_score
        low_user['rank'] = under_rank
    except:
        print("下位のプレイヤーが存在しません")

    if name:
        AccountData = Account.objects.get(username = name)
        user_icon = getUserIcon(AccountData)
        AccountData.recent_score = score
        if AccountData.best_score < score:
            AccountData.best_score = score
        corrects = request.session.get("correct_music", [])
        if corrects:
            for i in corrects:
                if i not in AccountData.correct_musics:
                    AccountData.correct_musics.append(i)
        AccountData.save()
    user = {'username': name, 'userIcon': user_icon, 'score': score, 'rank': rank}
    context = {
        'user': user,
        'high_user': high_user,
        'low_user': low_user,
    }
    return render(request, "musiq/result.html", context)

#問題ごとのデータセーブ
def Ingame_savedata(request):
    if request.method == "POST":
        isCorrect = int(request.POST.get("isCorrect"))
        answer_time = int(request.POST.get("answer_time"))

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
            del request.session["correct_music"][-1]
            request.session.save()
            
        if gamedata.current_question == 5:
            #終了時の処理
            Score = CalcScore(
                gamedata.correct, 
                gamedata.max_streak, 
                sum(gamedata.answer_times) / len(gamedata.answer_times)
            )
            print(f"Score: {Score}")
            request.session["score"] = Score
            return redirect(result)
        else:
            gamedata.current_question += 1

        gamedata.save()
        return redirect(game, gamedata.genre)
    else:
        return redirect(index)

#Spotify曲確認画面
def CheckSpotify(request):
    result_data = None
    form_data = {"title": "", "artist": ""}
    NotFound = None

    if request.method == "POST":
        form_data["title"] = request.POST.get("title")
        form_data["artist"] = request.POST.get("artist")
        query = f"track:{form_data['title']}"
        if form_data["artist"]:
            query += f" artist:{form_data['artist']}"
        
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

#ランキング画面
def ranking(request, page):
    users = Account.objects.all().order_by('-best_score')
    your_account = None
    sort_users = []
    account_data = {} 
    page_last = math.ceil(len(users) / 10) 
    start_rank = page * 10 - 9

    if request.session.get('username', None):
        your_account = Account.objects.get(username=request.session.get('username'))
        i = 1
        for user in users:
            if user.id == your_account.id:
                account_data["score"] = your_account.best_score
                account_data["icon"] = getUserIcon(your_account)
                account_data["rank"] = i
                break
            i += 1

    for i in range(10):
        rank = start_rank + i
        try:
            your_account_state = False
            if your_account:
                if users[rank -1].id == your_account.id:
                    your_account_state = True
            sort_users.append(
                {
                    "name": users[rank -1].username, 
                    "icon": getUserIcon(users[rank -1]),
                    "score": users[rank -1].best_score,
                    "rank": rank,
                    "state": your_account_state
                }
            )
        except:
            sort_users.append(
                {
                    "name": '-', 
                    "icon": settings.STATIC_URL + 'media/nologin.png',
                    "score": '-',
                    "rank": '-',
                    "state": False   
                }
            )           
    context = {
        "page": page,
        "next_page": page +1,
        "previous_page": page -1,
        "page_last": page_last,
        "users": sort_users,
        "your_account": account_data,
    }
    return render(request, "musiq/ranking.html", context)

#ルール画面
def rules(request):
    return render(request, "musiq/rules.html")

#マイページ画面
def mypage(request):
    name = request.session.get('username', None)
    userdata = Account.objects.get(username=name)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == "logout":
            try:
                del request.session['username']
            except:
                print("既にログアウトされています")
            return redirect(index)
        elif form_type == "changeIcon":
            user_icon = request.FILES.get('userIcon')
            if user_icon:
                userdata.userIcon = user_icon  
                userdata.save() 
            return redirect(mypage)
    
    sort_by_score = Account.objects.all().order_by('-best_score')
    rank = 1
    for i in sort_by_score:
        if i.id == userdata.id:
            break
        rank += 1
    if userdata.best_score == 0:
        rank = None
    userIcon = getUserIcon(userdata)
    context = {
        'user': userdata,
        'rank': rank, 
        'userIcon': userIcon,
        'corrects': len(userdata.correct_musics),
        'max_musics': len(musics),
    }
    return render(request, "musiq/mypage.html", context)

#マイページの名前変更画面
def rename(request):
    name = request.session.get('username', None)
    userdata = Account.objects.get(username=name)
    if request.method == 'POST':
        userdata.username = request.POST["name"]
        request.session['username'] = request.POST["name"]
        userdata.save()
        return redirect(mypage)

    return render(request, "musiq/mypage_rename.html", {'user': userdata})

