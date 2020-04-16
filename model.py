import poker
from poker import HeadsUpHand
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn import datasets
#*********** creating datasets **********************************
#all functions create a list of hands
# argument n - how many hands to create


#one hand, just for testing purposes
def printAHand():
  hand = HeadsUpHand()
  hand.printHand()

# preflop
def createPreflopData(n):
  preflopList = []
  for i in range(n):
    hand = HeadsUpHand()
    result = hand.heroWins() 
    hero1, hero2 = hand.heroCards
    element = hero1.tup(), hero2.tup(), result
    preflopList.append(element)
  return preflopList


# postflop
def createPostflopData(n):
  postflopList = []
  for i in range(n):
    hand = HeadsUpHand()
    result = hand.heroWins() 
    hero1, hero2 = hand.heroCards
    board = hand.board
    element = hero1.tup(), hero2.tup(), board[0].tup(), board[1].tup(), board[2].tup(), result
    postflopList.append(element)
  return postflopList


#turn
def createTurnData(n):
  turnList = []
  for i in range(n):
    hand = HeadsUpHand()
    result = hand.heroWins() 
    hero1, hero2 = hand.heroCards
    board = hand.board
    element = hero1.tup(), hero2.tup(), board[0].tup(), board[1].tup(), board[2].tup(), board[3].tup(), result
    turnList.append(element)
  return turnList


#river
def createRiverData(n):
  riverList = []
  for i in range(n):
    hand = HeadsUpHand()
    result = hand.heroWins() 
    hero1, hero2 = hand.heroCards
    board = hand.board
    element = hero1.tup(), hero2.tup(), board[0].tup(), board[1].tup(), board[2].tup(), board[3].tup(), board[4].tup(), result
    riverList.append(element)
  return riverList


#******** creating a tensorflow model *****************************************

def createModel(n):

  #create the dataset
  data = createPostflopData(n)
  element_length = len(data[0])
  y_vals = np.array([x[-1] for x in data]) #labels
  x_vals = np.array([x[0:element_length - 1] for x in data]) #features

  #split the data into train and test 
  x_train, x_test, y_train, y_test = train_test_split(x_vals, y_vals, test_size = 0.2)

  #labels are categorical
  y_train = keras.utils.to_categorical(y_train, 3)
  y_test = keras.utils.to_categorical(y_test, 3)

  #start session
  sess = tf.Session()