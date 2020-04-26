from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Game
# Create your views here.

def splash(request):
    return render(request, 'splash.html', {})

def accounts(request):
    return render(request, 'accounts.html')

def board(request):
    game = Game.objects.get(player=request.user.username)
    
    return render(request, 'board.html', 
        {"hand" : ["2(d)", "7(h)"], "botHand" : ["A(s)", "A(h)"], "board" : ["2(h)", "7(d)", "7(c)", "A(c)", "K(s)"], "pot" : 120})

def load_game(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/board")

    return render(request, 'accounts.html', {"message" : "incorrect username/password"})

def new_game(request):
    username = request.POST['username']
    password = request.POST['password']

    user = User.objects.create_user(username=request.POST['username'],
					password=request.POST['password'])
    login(request, user)
    return redirect('/board')

def logout(request):
    logout(request)
    return redirect("/accounts")

def check(request):
    return redirect('/board')

def bet(request):
    return redirect('/board')

def fold(request):
    return redirect('/board')

