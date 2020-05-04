from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.

class Card(models.Model):
    suit = models.BigIntegerField(default=0)
    value = models.BigIntegerField(default=0)

    def __str__(self):
        #get value
        val = ""
        if (self.value < 10):
            val = str(self.value)
        elif (self.value == 14):
            val = "A"
        elif (self.value == 11):
            val = "J"
        elif (self.value == 10):
            val = "10"
        elif (self.value == 12):
            val = "Q"
        elif (self.value == 13):
            val = "K"
        
        #get suit
        st = ""
        if (self.suit == 1):
            st = "(s)"
        elif (self.suit == 2):
            st = "(c)"
        elif (self.suit == 3):
            st = "(h)"
        elif (self.suit == 4):
            st = "(d)"

        return val + st 

class Hand(models.Model):
    cards = models.ManyToManyField('Card')

    def __str__(self):
        displayString = ""

        for card in self.cards.all():
            displayString += str(card) + " "

        return displayString[0: len(displayString) - 1]

class Board(models.Model):
    player = models.CharField(max_length=100, default="player_name")
    cards = models.ManyToManyField('Card')

    def __str__(self):
        displayString = ""

        for card in self.cards.all():
            displayString += str(card) + "\t"

        return displayString[0:len(displayString) - 1]

    def getFlop(self):
        displayString = ""

        i = 0

        for card in self.cards.all():
            if i == 3:
                break

            i += 1
            displayString += str(card) + "\t"

        return displayString

    def getTurn(self):
        displayString = ""

        i = 0

        for card in self.cards.all():
            if i == 4:
                break
            
            i += 1
            displayString += str(card) + "\t"


        return displayString[0:len(displayString) - 1]

    def getRiver(self):
        displayString = ""

        i = 0

        for card in self.cards.all():
            i += 1
            displayString += str(card) + "\t"


        return displayString[0:len(displayString) - 1]

class Deck(models.Model):
    cards = models.ManyToManyField('Card')

    def deal(self):
        cardSet = self.cards.all() 

        for card in cardSet:
            self.cards.remove(card)
            print("THIS IS CARD " + str(card.value) + " " + str(card.suit))
            return card

    def __str__(self):
        displayString = ""

        for card in cards.all():
            displayString += str(card) + " "

        return displayString[0: len(displayString) - 1]

class Game(models.Model):
    
    player_name = models.CharField(max_length=100, default="player_name")
    player = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    numWins = models.BigIntegerField(default=0)

    player_hand = models.OneToOneField('Hand', on_delete=models.DO_NOTHING, related_name="player")
    player_stack = models.BigIntegerField(default=0)
    player_bet = models.BigIntegerField(default=0)

    bot_hand = models.OneToOneField('Hand', on_delete=models.DO_NOTHING, related_name="bot")
    bot_stack = models.BigIntegerField(default=0)
    bot_bet = models.BigIntegerField(default=0)

    pot = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    street = models.BigIntegerField(default=0)

    blinds = models.BigIntegerField(default=0)

    board = models.OneToOneField('Board', on_delete=models.DO_NOTHING, related_name="board")

    def __str__(self):
        return self.player_name