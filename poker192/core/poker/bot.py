from . import poker 
from . import model 
from .datasets import getTuple
import numpy as np
import tensorflow as tf
import keras 

# int for street
# list for hand
# list for board

def predict(street, board, heroCards):
    #get all of the cards
    hero1 = heroCards[0] 
    hero1s = hero1.suit
    hero1v = hero1.value
    hero2 = heroCards[1] 
    hero2s = hero2.suit
    hero2v = hero2.value
    if street >= 1: 
        board1 = board[0] 
        board1s = board1.suit
        board1v = board1.value
        board2 = board[1] 
        board2s = board2.suit
        board2v = board2.value
        board3 = board[2] 
        board3s = board3.suit
        board3v = board3.value
    if street >= 2: 
        board4 = board[3] 
        board4s = board4.suit
        board4v = board4.value
    if street >= 3: 
        board5 = board[4] 
        board5s = board5.suit
        board5v = board5.value

    element = None
    #make the element to predict
    if street == 0:
        element = hero1v, hero1s, hero2v, hero2s
    elif street == 1: 
        element = hero1v, hero1s, hero2v, hero2s, board1v, board1s, board2v, board2s, board3v, board3s
    elif street == 2:
        element = hero1v, hero1s, hero2v, hero2s, board1v, board1s, board2v, board2s, board3v, board3s, board4v, board4s
    elif street == 3:
        element = hero1v, hero1s, hero2v, hero2s, board1v, board1s, board2v, board2s, board3v, board3s, board4v, board4s, board5v, board5s
    else:
        return None
    
    #wrap the element in a list
    list_wrapper = []
    list_wrapper.append(element)
    list_wrapper = np.array(list_wrapper)

    #load the model
    model = None

    if street == 0:
        model = tf.keras.models.load_model('./saved_models/preflop_model')
    elif street == 1: 
        model = tf.keras.models.load_model('./saved_models/postflop_model')
    elif street == 2:
        model = tf.keras.models.load_model('./saved_models/turn_model')
    elif street == 3:
        model = tf.keras.models.load_model('./saved_models/river_model')
    else:
        return None

    #predict
    result = model.predict_classes(list_wrapper)


    result = result[0]

    if result == 0:
        return 0
    if result == 1:
        return 1
    if result == 2:
        return -1
