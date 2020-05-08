from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Game, Deck, Hand, Card, Board
from core.poker.poker import HeadsUpHand
from core.poker import bot, poker
import random
# Create your views here.

def splash(request):
    return render(request, 'splash.html', {})

def board(request): #render the board
    game = Game.objects.get(player_name=request.user.username)

    check_status = False #is check allowed (is there a raise)
    show_vil = False #do we reveal the villain cards
    bot_hand_type = ""
    player_hand_type = ""

    if game.player_bet == game.bot_bet:
        game.player_bet = 0
        game.bot_bet = 0
        game.save()
        check_status = True

    hand = game.player_hand
    bot_hand = game.bot_hand
    board = game.board
    pot = game.pot
    bot_stack = game.bot_stack
    stack = game.player_stack
    player_bet = game.player_bet
    bot_bet = game.bot_bet
    street = game.street
    game_status = False
    message = ""

    streetName = ""
    boardDisplay = ""

    if street == 0: #determine board
        boardDisplay = ""
        streetName = "pre-flop"
    elif street == 1:
        boardDisplay = board.getFlop
        streetName = "flop"
    elif street == 2:
        boardDisplay = board.getTurn
        streetName = "turn"
    elif street == 3:
        boardDisplay = board.getRiver
        streetName = "river"
    elif street == 4: #showdown

        streetName = "showdown"
        show_vil = True

        boardDisplay = board.getRiver
        bot_cards = game.bot_hand.cards.all()
        player_cards = game.player_hand.cards.all()
        board_cards = game.board.cards.all()
        
        #check who wins, 1-player, 0-chop, -1-villain
        showdown_value, pht, bht = poker.whoWins(bot_cards, player_cards, board_cards)

        player_hand_type = pht
        bot_hand_type = bht

        if showdown_value == -1:
            game.bot_stack += pot
            game.pot = 0
            message = "villain wins"

            if game.player_stack == 0:
                game_status = True
        elif showdown_value == 0:
            half_pot = game.pot // 2
            game.pot = 0
            game.player_stack += half_pot
            game.bot_stack += half_pot
            message = "chop"
        else: #showdown value is 1, player wins
            game.player_stack += pot
            game.pot = 0
            message = "you win!"
            if game.bot_stack == 0:
                game_status = True
        
        game.save()
        
    else:
        boardDisplay = "error in board street"

    return render(request, 'board.html', 
        {"hand" : str(hand), "botHand" : str(bot_hand), "board" : boardDisplay, \
            "pot" : pot, "playerName" : request.user.username, "stack" : stack, \
            "playerBet" : player_bet, "botBet" : bot_bet, "botStack" : bot_stack, \
            "street" : streetName, "streetNo" : street, "message" : message, \
            "gameComplete" : game_status, "canCheck" : check_status, "showVil" : show_vil, \
            "botHandType" : bot_hand_type, "playerHandType" : player_hand_type})

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
    game.street = 0
    newDeck = Deck()
    newDeck.save()

    #shuffle the deck and put it into the db
    cardTuples = [(i, j) for i in range(2, 15) for j in range(1, 5)] 
    random.shuffle(cardTuples)

    for (i, j) in cardTuples:
        newCard = Card(value=i, suit=j)
        newCard.save()
        newDeck.cards.add(newCard)

    x1, x2 = newDeck.deal(), newDeck.deal()
    y1, y2 = newDeck.deal(), newDeck.deal()

    #deal players new cards
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

    #deal 5 cards for the board
    boardCards = [newDeck.deal() for i in range(5)]

    for bc in boardCards:
        board.cards.add(bc)
    
    game.player_hand = playerHand
    game.bot_hand = botHand
    game.pot = 0
    game.board = board
    game.player_bet = min(game.blinds, game.player_stack)
    game.bot_bet = min(game.blinds, game.bot_stack)
    game.player_stack -= game.player_bet
    game.bot_stack -= game.bot_bet

    game.pot = game.player_bet + game.bot_bet

    game.save()

    return redirect('/board')

def next_game(request):

    game = Game.objects.get(player_name=request.user.username)

    og_stack = (max(game.player_stack, game.bot_stack) + game.blinds) // 2 

    #reset stacks
    game.player_stack = og_stack
    game.bot_stack = og_stack
    
    game.street = 0

    game.save()

    return redirect('/newhand')

def new_game(request):

    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    stack = int(request.POST['stack_amount'])
    blinds = int(stack // 75)

    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)

    newDeck = Deck()
    newDeck.save()

    #new deck
    cardTuples = [(i, j) for i in range(2, 15) for j in range(1, 5)] 
    random.shuffle(cardTuples)

    for (i, j) in cardTuples:
        newCard = Card(value=i, suit=j)
        newCard.save()
        newDeck.cards.add(newCard)

    x1, x2 = newDeck.deal(), newDeck.deal()
    y1, y2 = newDeck.deal(), newDeck.deal()

    #deal players new hand
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

    newGame = Game(player_name=request.user.username, player=request.user,\
        player_stack=stack, bot_stack=stack, player_hand=playerHand, \
            bot_hand=botHand, board=board, street=0, blinds=blinds)
    
    newGame.save()

    #start a new hand
    return redirect('/newhand')

def logout(request):
    logout(request)
    return redirect("/splash")

def call(request):
    game = Game.objects.get(player_name=request.user.username)

    if game.street != 4: #check not on showdown
        if game.player_bet < game.bot_bet:
            bot_bet = game.bot_bet

            player_stack = game.player_stack

            diff = bot_bet - game.player_bet

            if player_stack < diff: #player all in
                back_to_bot = diff - player_stack
                game.bot_stack += back_to_bot
                game.pot -= back_to_bot
                game.bot_bet = player_stack
                game.player_bet = player_stack
                game.player_stack = 0
                game.pot += player_stack
            else: #normal bet
                game.player_stack -= diff
                game.player_bet = game.bot_bet
                game.pot += diff

            #either player all in -> goes to showdown
            if game.player_stack == 0 or game.bot_stack == 0:
                game.street = 4
            else: #advance street if call
                game.street += 1

            game.save()

    return redirect('/board')

def check(request):

    game = Game.objects.get(player_name=request.user.username)

    #check if either player is all in
    if game.bot_stack == 0 or game.player_stack == 0:
        game.street = 4

    if game.street != 4: #check not in showdown yet
        if game.player_bet >= game.bot_bet: 
            bot_cards = game.bot_hand.cards.all()

            board_cards = game.board.cards.all()

            street = game.street

            #get bot's predict value
            predict_value = bot.predict(street, board_cards, bot_cards)

            if predict_value == 1: #bot bets
                bot_stack = game.bot_stack
                bot_bet = 0

                if game.pot == 0:
                    bot_bet = max(bot_stack // 20, game.blinds * 2)
                    game.bot_stack -= bot_bet
                else:
                    bot_bet = min(game.pot // 3, bot_stack)
                    game.bot_stack -= bot_bet
                
                game.bot_bet = bot_bet
                game.pot += bot_bet

                game.save()

            elif predict_value == 0: #bot calls
                game.street += 1

                game.save()
            elif predict_value == -1: #bot calls
                game.street += 1

                game.save()
            else:
                print("error in predict value")

    return redirect('/board')

def bet(request):
    betAmt = int(request.POST['amt'])

    game = Game.objects.get(player_name=request.user.username)

    if game.street != 4:
        player_stack = game.player_stack

        #player can only bet up to the amt of stack
        if betAmt > player_stack:
            game.player_bet = betAmt
            game.player_stack = 0
            game.street = 4

            return redirect('/board')
        else:
            game.player_stack = player_stack - betAmt
        
        game.pot += betAmt

        game.player_bet = betAmt

        bot_cards = game.bot_hand.cards.all()

        board_cards = game.board.cards.all()

        street = game.street

        #get bot's predict value
        predict_value = bot.predict(street, board_cards, bot_cards)

        if predict_value == 1:
            bot_stack = game.bot_stack
            bot_bet = 0

            #bot reraises
            bot_bet = min(game.player_bet * 3 // 2, bot_stack)

            if bot_bet < game.player_bet:
                back_to_player = game.player_bet - bot_bet
                game.pot -= back_to_player
                game.pot += bot_bet
                game.player_bet -= back_to_player
                game.player_stack += back_to_player
                game.bot_stack -= bot_bet
                game.bot_bet = bot_bet
                game.street = 4
                game.save()

                return redirect('/board')

            game.bot_stack -= bot_bet
            
            game.bot_bet = bot_bet
            game.pot += bot_bet

            if game.bot_stack == 0 or game.player_stack == 0:
                game.street = 4

            game.save()

            return redirect('/board')

        elif predict_value == 0:
            #bot flat-calls if predict value is 0
            diff = game.player_bet - game.bot_bet

            bot_bet = min(game.bot_stack, diff)

            if bot_bet < game.player_bet:
                back_to_player = game.player_bet - bot_bet
                game.pot -= back_to_player
                game.player_bet -= back_to_player
                game.player_stack += back_to_player
                game.street = 4
                return redirect('/board')

            game.bot_bet += bot_bet
            game.pot += bot_bet
            game.bot_stack -= bot_bet

            game.street += 1

            game.save()

            return redirect('/board')
        elif predict_value == -1:
            #bot folds
            game.player_stack += game.pot
            game.pot = 0
            game.player_bet = 0
            game.bot_bet = 0
            game.save()
            return redirect('/newhand')
        else:
            print("error in predict value")

        game.save()

    return redirect('/board')

def fold(request):
    game = Game.objects.get(player_name=request.user.username)
    if game.street != 4: 
        #reset game parameters
        game.bot_stack += game.pot
        game.pot = 0
        game.bot_bet = 0
        game.player_bet = 0
        game.street = 0

        game.save()

        return redirect('/newhand')
    else:
        return redirect('/board')
    

