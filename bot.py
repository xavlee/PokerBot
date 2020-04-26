import poker
import model
import datasets
from datasets import getTuple
import numpy as np
import tensorflow as tf
import keras 

def predict(street, board, heroCards):
    #get all of the cards
    hero1, hero2 = heroCards
    hero1v, hero1s = getTuple(hero1) 
    hero2v, hero2s = getTuple(hero2)
    if len(board) >= 3: 
        board1v, board1s = getTuple(board[0])
        board2v, board2s = getTuple(board[1])
        board3v, board3s = getTuple(board[2])
    if len(board) >= 4: 
        board4v, board4s = getTuple(board[3])
    if len(board) >= 5: 
        board5v, board5s = getTuple(board[4])

    element = None
    #make the element to predict
    if street == 'preflop':
        element = hero1v, hero1s, hero2v, hero2s
    elif street == 'postflop': 
        element = hero1v, hero1s, hero2v, hero2s, board1v, board1s, board2v, board2s, board3v, board3s
    elif street == 'turn':
        element = hero1v, hero1s, hero2v, hero2s, board1v, board1s, board2v, board2s, board3v, board3s, board4v, board4s
    elif street == 'river':
        element = hero1v, hero1s, hero2v, hero2s, board1v, board1s, board2v, board2s, board3v, board3s, board4v, board4s, board5v, board5s
    else:
        return None
    
    #wrap the element in a list
    list_wrapper = []
    list_wrapper.append(element)
    list_wrapper = np.array(list_wrapper)

    #load the model
    model_filename = None
    if street == 'preflop':
        model_filename = 'preflop_model'
    elif street == 'postflop': 
        model_filename = 'postflop_model'
    elif street == 'turn':
        model_filename = 'turn_model'
    elif street == 'river':
        model_filename = 'river_model'
    else:
        return None

    model = tf.keras.models.load_model(model_filename) 


    #predict
    result = model.predict_classes(list_wrapper)


    result = result[0]

    if result == 0:
        return 0
    if result == 1:
        return 1
    if result == 2:
        return -1
