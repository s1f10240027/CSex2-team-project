from django.views.generic.base import RedirectView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("SelectGenre", views.select_genre, name="select_genre"),
    path("Game", RedirectView.as_view(pattern_name="select_genre"), name="game_novalue"),
    path("Game/<value>", views.game, name="game"),
    path("Ranking/<int:page>", views.ranking, name="ranking"),
    path("GameInfo", views.rules, name="rules"),
    path('Ingame_savedata', views.Ingame_savedata, name='Ingame_savedata'),
    path('login', views.login_view, name="login"),
    path("Mypage", views.mypage, name="mypage"),
    path("Mypage/rename", views.rename, name="rename"),
    path("result", views.result, name="result"),
    path("retry", views.retry, name="retry"),
    path("Info", views.rules, name="rules"), 
    path("spotify", views.CheckSpotify, name="CheckSpotify"),
]