from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("SelectGenre", views.select_genre, name="select_genre"),
    path("Ranking", views.ranking, name="ranking"),
    path("GameInfo", views.rules, name="rules"),
    path("spotify", views.CheckSpotify, name="CheckSpotify"),
]