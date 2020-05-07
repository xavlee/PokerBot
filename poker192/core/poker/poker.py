## j - 11; q - 12; k-13, a - 14
#spades - 1, clubs - 2; hearts - 3; diamonds - 4 
#high card - 1
#pair - 2
#two pair - 3
#trips - 4
#straight - 5
#flush - 6
#boat - 7
#quads - 8
#straight flush - 9

#************************** imports ******************************

import random
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn import datasets
from math import floor

#******************* Poker game **********************************

def printBoard(board):
    for card in board:
        print(" " + str(card) + " ")

class Card: 
    def __init__(self, val, st):
        self.value = val
        self.suit = st 

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
            val = "T"
        elif (self.value == 12):
            val = "Q"
        elif (self.value == 13):
            val = "K"
        
        #get suit
        st = ""
        if (self.suit == 1):
            st = "s"
        elif (self.suit == 2):
            st = "c"
        elif (self.suit == 3):
            st = "h"
        elif (self.suit == 4):
            st = "d"

        return val + st 

    def tup(self):
      return self.value, self.suit


    
class Deck:
    def __init__(self):
        self.cards = [Card(i, j) for i in range(2, 15) for j in range(1, 5)]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

        

class Pair:
    def __init__(self, numOfCards, valOfCard):
        self.num = numOfCards
        self.val = valOfCard

def getValue(card):
    if (isinstance(card, Card)):
        return card.value
    else:
        return card 

def getHighCard(cards, cantbe, numNeeded):

  if (isinstance(cards[0], Card)):

    cardscopy = cards.copy()

    cardscopy.sort(key= getValue)
    highest = [] 

    while len(highest) < numNeeded:
      highest.append(cardscopy.pop().value)
      tot = 0
    for i in range(numNeeded):
      tot += (highest[i] / (10**i))
    return tot
  else:
    cardscopy = cards.copy()
    cardscopy.sort()
    highest = [] 

    while len(highest) < numNeeded:
      highest.append(cardscopy.pop())
    tot = 0
    for i in range(numNeeded):
      tot += (highest[i] / (10**i))
    return tot




def hasPairs(cards):
    
    nums = [0]*15 
    for card in cards:
        nums[card.value] += 1

    pairs = [] 

    i = 14
    while i > 1:
        if nums[i] > 1:
            pairs.append(Pair(nums[i], i))
        i -= 1


    if len(pairs) == 3:
        pair1N, pair1V = pairs[0].num, pairs[0].val
        pair2N, pair2V = pairs[1].num, pairs[1].val
        pair3N, pair3V = pairs[2].num, pairs[2].val

        # check if there is a full house
        if pair1N == 3:
            return 7 + pair1V / 100 + pair2V / 10000 
        if pair2N == 3:
            return 7 + pair2V / 100 + pair1V / 10000
        if pair3N == 3:
            return 7 + pair3V / 100 + pair1V / 10000

        #return value of two pair
        tot = 3
        tot += (pair1V / 100) 
        tot += (pair2V / 10000)
        highCard = getHighCard(cards, [pair1V, pair2V], 1)
        return tot + (highCard / 1000000)

    if len(pairs) == 2:
        pair1N, pair1V = pairs[0].num, pairs[0].val
        pair2N, pair2V = pairs[1].num, pairs[1].val

        #check for quads
        if pair1N == 4: 
            return 8 + (pair1V / 100) + getHighCard(cards, pair1V, 1)
        if pair2N == 4: 
            return 8 + (pair2V / 100) + getHighCard(cards, pair2V, 1)


        # check if there is a full house
        if pair1N == 3:
            return 7 + pair1V / 100 + pair2V / 10000 
        if pair2N == 3:
            return 7 + pair2V / 100 + pair1V / 10000

        #return value of two pair
        tot = 3
        tot += (pair1V / 100) 
        tot += (pair2V / 10000)
        highCard = getHighCard(cards, [pair1V, pair2V], 1)
        return tot + (highCard / 1000000)

    if len(pairs) == 1:
        
        pairN, pairV = pairs[0].num, pairs[0].val 

        #check for quads
        if pairN == 4: 
            return 8 + (pairV / 100) + (getHighCard(cards, pairV, 1) / 10000) 

        #check for trips
        if pairN == 3: 
            return 4 + (pairV / 100) + (getHighCard(cards, pairV, 2) / 10000)

        #return value of pair
        return 2 + (pairV / 100) + (getHighCard(cards, pairV, 3) / 10000) 

    return 1 + (getHighCard(cards, [], 5) / 100)  

#returns -1 if no straight, or the value of the highest card in the straight if there is a straight 
def hasStraight(cards):
    cardscopy = cards.copy()
    if (isinstance(cardscopy[0], Card)):
      cardscopy = [card.value for card in cardscopy]


    cardscopy.sort(key= getValue)
    #copy aces so they are low and high 
    
    for card in cards:
        if card == 14:
            cardscopy.insert(0, card)


    straightLength = 0
    highestCardStraight = -1
    prevVal = -1

    for card in cardscopy:
        # case where this is first card
        if prevVal == -1:
            prevVal = card
            straightLength = 1

        # case where the straight continues
        elif prevVal == card - 1 or (prevVal == 14 and card == 2):
            straightLength += 1
            prevVal = card

        #case where repeat card so straight stays
        elif prevVal == card:
            continue 

        # case where the straight ends
        else:
            if straightLength >= 5:
                highestCardStraight = prevVal
            straightLength = 1
            prevVal = card

    if straightLength >= 5:
        highestCardStraight = prevVal 

    return highestCardStraight



def hasStraightFlush(cards): 

    #CHECK IF THERE IS A FLUSH
    clubs = []
    spades = []
    hearts = []
    diamonds = []
    flushNum = -1
    flushCards = []

    for card in cards:
        if card.suit == 1:
            spades.append(card.value)
            if len(spades) >= 5:
                flushNum = 1
        if card.suit == 2:
            clubs.append(card.value)
            if len(clubs) >= 5:
                flushNum = 2
        if card.suit == 3:
            hearts.append(card.value)  
            if len(hearts) >= 5:
                flushNum = 3  
        if card.suit == 4:
            diamonds.append(card.value)
            if len(diamonds) >= 5:
                flushNum = 4

    if not (flushNum == -1):
        if flushNum == 1:
            flushCards = spades
        if flushNum == 2:
            flushCards = clubs 
        if flushNum == 3:
            flushCards = hearts
        if flushNum == 4:
            flushCards = diamonds 


    
    #check if there is a straight
    highestCardStraight = hasStraight(cards) 


    #check if there is a straight flush
    higestCardStraightFlush = -1
    if (not highestCardStraight == -1) and (not flushNum == -1):
        highestCardStraightFlush = hasStraight(flushCards) 
        

    #if there is a straight flush
    if not (higestCardStraightFlush == -1):
        return 9 + (highestCardStraightFlush / 100) 
    
    elif not (flushNum == -1): 
      if len(flushCards) < 5:
        print("less than 5" + str(len(flushCards)))
      return 6 + (getHighCard(flushCards, [], 5) / 1000)

    elif not (highestCardStraight == -1):
        return 5 + (highestCardStraight / 100)

    else: 
        return 0

    
def handValue(holeCards, boardCards):

    hole1, hole2 = holeCards
    cardsPair = [hole1, hole2]
    cardsStraight = [hole1, hole2]
    for i in boardCards:
        cardsPair.append(i)
        cardsStraight.append(i)

    straightFlushVal = hasStraightFlush(cardsStraight)
    pairsVal = hasPairs(cardsPair) 
    return max(pairsVal, straightFlushVal)



class HeadsUpHand:
    def __init__(self, board=None, heroCards=None, vilCards=None):
        self.deck = Deck()

        if board is None:
            self.board = []
        else:
            self.board = board

        if heroCards is None:
            self.heroCards = self.deck.deal(), self.deck.deal()
        else:
            self.heroCards = heroCards

        if vilCards is None:
            self.vilCards = self.deck.deal(), self.deck.deal()   
        else:
            self.vilCards = vilCards

    def flop(self):
        for i in range(3):
            self.board.append(self.deck.deal())

    def turn(self):
        while len(self.board) < 4:
            self.board.append(self.deck.deal())

    def river(self):
        while len(self.board) < 5:
            self.board.append(self.deck.deal())

    def heroWins(self):
        self.river()
        heroValue = handValue(self.heroCards, self.board)
        villainValue = handValue(self.vilCards, self.board)
        if (heroValue > villainValue):
            return 1
        elif (heroValue == villainValue):
            return 0
        else:
            return -1

    def printHand(self):
        print("")
        print("result: " + str(self.heroWins()))
        hero1, hero2 = self.heroCards
        vil1, vil2 = self.vilCards

        print("hero cards: " + str(hero1) + " " + str(hero2))
        print("vill cards: " + str(vil1) + " " + str(vil2))
        self.board.sort(key= getValue)
        printBoard(self.board)



#playercards - 

#1 if player wins
#0 if chop
#-1 if bot wins
def whoWins(botCards, playerCards, boardCards):
    #make cards for this file
    player1 = Card(playerCards[0].value, playerCards[0].suit)
    player2 = Card(playerCards[1].value, playerCards[1].suit)
    bot1 = Card(botCards[0].value, botCards[0].suit)
    bot2 = Card(botCards[1].value, botCards[1].suit)
    board1 = Card(boardCards[0].value, boardCards[0].suit)
    board2 = Card(boardCards[1].value, boardCards[1].suit)
    board3 = Card(boardCards[2].value, boardCards[2].suit)
    board4 = Card(boardCards[3].value, boardCards[3].suit)
    board5 = Card(boardCards[4].value, boardCards[4].suit)
    
    #make arguments for score function
    boardList = [board1, board2, board3, board4, board5]
    playerTuple = player1, player2
    botTuple = bot1, bot2

    #get scores
    playerScore = handValue(playerTuple, boardList)
    botScore = handValue(botTuple, boardList)

    playerRounded = floor(playerScore)
    botRounded = floor(botScore)

    playerString = "Nothing"
    botString = "Nothing"

#high card - 1
#pair - 2
#two pair - 3
#trips - 4
#straight - 5
#flush - 6
#boat - 7
#quads - 8
#straight flush - 9

    if playerRounded == 1:
        playerString = "High Card"
    elif playerRounded == 2:
        playerString = "Pair"
    elif playerRounded == 3:
        playerString = "Two Pair"
    elif playerRounded == 4:
        playerString = "Trips"
    elif playerRounded == 5:
        playerString = "Straight"
    elif playerRounded == 6:
        playerString = "Flush"
    elif playerRounded == 7:
        playerString = "Full House"
    elif playerRounded == 8:
        playerString = "Quads"
    elif playerRounded >= 9:
        playerString = "Straight Flush" 

    if botRounded == 1:
        botString = "High Card"
    elif botRounded == 2:
        botString = "Pair"
    elif botRounded == 3:
        botString = "Two Pair"
    elif botRounded == 4:
        botString = "Trips"
    elif botRounded == 5:
        botString = "Straight"
    elif botRounded == 6:
        botString = "Flush"
    elif botRounded == 7:
        botString = "Full House"
    elif botRounded == 8:
        botString = "Quads"
    elif botRounded >= 9:
        botString = "Straight Flush"

    winner = 0

    if playerScore > botScore:
        winner = 1
    elif botScore > playerScore:
        winner = -1

    #return something
    return winner, playerString, botString
