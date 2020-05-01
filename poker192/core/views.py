from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Game, Deck, Hand, Card, Board
from core.poker.poker import HeadsUpHand
import random
# Create your views here.

def splash(request):
    return render(request, 'splash.html', {})

def accounts(request):
    return render(request, 'accounts.html')

def board(request):
    game = Game.objects.get(player_name=request.user.username)

    hand = game.player_hand
    bot_hand = game.bot_hand
    board = game.board
    pot = game.pot
    bot_stack = game.bot_stack
    stack = game.player_stack
    player_bet = game.player_bet
    bot_bet = game.bot_bet
    
    return render(request, 'board.html', 
        {"hand" : str(hand), "botHand" : str(bot_hand), "board" : str(board), \
            "pot" : pot, "playerName" : request.user.username, "stack" : stack, \
            "playerBet" : player_bet, "botBet" : bot_bet, "botStack" : bot_stack})

def load_game(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/board")

    return render(request, 'accounts.html', {"message" : "incorrect username/password"})

def new_hand(request):
    game = Game.objects.get(player_name=request.user.username)

    newDeck = Deck()
    newDeck.save()

    cardTuples = [(i, j) for i in range(2, 15) for j in range(1, 5)] 
    random.shuffle(cardTuples)

    for (i, j) in cardTuples:
        newCard = Card(value=i, suit=j)
        newCard.save()
        newDeck.cards.add(newCard)

    x1, x2 = newDeck.deal(), newDeck.deal()
    y1, y2 = newDeck.deal(), newDeck.deal()

    playerHand = Hand()
    playerHand.save()
    playerHand.cards.add(x1)
    playerHand.cards.add(x2)

    botHand = Hand()
    botHand.save()
    botHand.cards.add(y1)
    botHand.cards.add(y2)

    board = Board(player=request.user)
    board.save()

    boardCards = [newDeck.deal() for i in range(5)]

    for bc in boardCards:
        board.cards.add(bc)
    
    game.player_hand = playerHand
    game.bot_hand = botHand
    game.pot = 0
    game.board = board

    game.save()

    return redirect('/board')

def new_game(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    stack = int(request.POST['stack_amount'])

    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)

    newDeck = Deck()
    newDeck.save()

    cardTuples = [(i, j) for i in range(2, 15) for j in range(1, 5)] 
    random.shuffle(cardTuples)

    for (i, j) in cardTuples:
        newCard = Card(value=i, suit=j)
        newCard.save()
        newDeck.cards.add(newCard)

    x1, x2 = newDeck.deal(), newDeck.deal()
    y1, y2 = newDeck.deal(), newDeck.deal()

    playerHand = Hand()
    playerHand.save()
    playerHand.cards.add(x1)
    playerHand.cards.add(x2)

    botHand = Hand()
    botHand.save()
    botHand.cards.add(y1)
    botHand.cards.add(y2)

    board = Board(player=request.user)
    board.save()

    boardCards = [newDeck.deal() for i in range(5)]

    for bc in boardCards:
        board.cards.add(bc)

    newGame = Game(player_name=request.user.username, player=request.user, player_stack=stack, \
        bot_stack=stack, player_hand=playerHand, bot_hand=botHand, board=board)
    
    newGame.save()

    return redirect('/board')

def logout(request):
    logout(request)
    return redirect("/accounts")

def check(request):

    game = Game.objects.get(player_name=request.user.username)

    if game.player_bet == game.bot_bet:
        return redirect('/board')

    player_stack = game.player_stack

    if player_stack < game.bot_bet - game.player_bet:
        game.player_bet = player_stack
        game.player_stack = 0
    else:
        game.player_stack -= (game.bot_bet - game.player_bet)
        game.player_bet = game.bot_bet

    game.save()

    return redirect('/board')

def bet(request):
    betAmt = int(request.POST['amt'])

    game = Game.objects.get(player_name=request.user.username)

    player_stack = game.player_stack

    if betAmt > player_stack:
        if betAmt < game.bot_bet:
            return redirect('/board')

        betAmt = player_stack
        game.player_stack = 0
    else:
        game.player_stack = player_stack - betAmt
    
    game.pot += betAmt

    game.player_bet = betAmt

    game.save()

    return redirect('/board')

def fold(request):
    game = Game.objects.get(player_name=request.user.username)

    game.bot_stack += game.pot
    game.pot = 0
    game.bot_bet = 0
    game.player_bet = 0

    game.save()

    return redirect('/newhand')

