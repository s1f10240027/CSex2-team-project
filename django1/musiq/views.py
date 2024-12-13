from django.shortcuts import render

def index(request):
    return render(request, "musiq/index.html")

def select_genre(request):
    return render(request, "musiq/select_genre.html")

def ranking(request):
    return render(request, "musiq/ranking.html")

def rules(request):
    return render(request, "musiq/rules.html")