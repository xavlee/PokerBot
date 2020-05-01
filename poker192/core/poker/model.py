# poker stuff
from .poker import HeadsUpHand

#datasets stuff
from .datasets import createHandData

# data stuff 
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split

#tensorflow stuff
import tensorflow as tf
import keras 
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD


#******** creating a tensorflow model *****************************************

def createModel(n, street):

  in_dim = 0

  if street == 'preflop':
    in_dim = 4
  elif street == 'postflop': 
    in_dim = 10
  elif street == 'turn':
    in_dim = 12
  elif street == 'river':
    in_dim = 14
  else:
    return None


  #create the dataset
  data = createHandData(n, street)

  element_length = len(data[0])
  y_vals = np.array([x[-1] for x in data]) #labels
  x_vals = np.array([x[0:element_length - 1] for x in data]) #features

  #split the data into train and test 
  trainX, testX, trainy, testy = train_test_split(x_vals, y_vals, test_size = 0.2)

  #labels are categorical
  trainy = keras.utils.to_categorical(trainy, 3)
  testy = keras.utils.to_categorical(testy, 3)

  # define model
  model = Sequential()
  model.add(Dense(50, input_dim=in_dim, activation='relu', kernel_initializer='he_uniform'))
  model.add(Dense(3, activation='softmax'))

  # compile model
  opt = SGD(lr=0.01, momentum=0.9)
  model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

  # fit model
  model.fit(trainX, trainy, validation_data=(testX, testy), epochs=5, verbose=0)

  return model