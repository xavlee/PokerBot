# CIS 192 Final: Pokerbot
For our final project, we implemented a Tensorflow-driven pokerbot. 
## Game and Model: poker192/core/poker
### The Game: poker.py
The first step of the process was to implement poker. For simplicity, and to give the bot the best chance to win, we decided to make the game heads up (one on one). We built simple functions to simulate a game, including a card class, a deck class, and the main challenge in this section: a function to determine who won a particular hand.  
### The Data: datasets.py
To train our model, we needed lots of data. Thus, we wrote a function that created datasets of simulated poker hands for us. The data simply consisted of a user hand, a bot hand, a board, and whether the bot won, lost, or tied. 
### The Models: model.py
In this file, tensorflow models were created and saved. There were four different models created, one for each street: preflop, flop, turn and river. For each street, the bot was trained on only what a player would be able to see on that street. For example, in the flop model, the bot was trained on two hole cards and three board cards. The label on each hand was whether the bot won, lost, or tied. The bot was clearly not shown the opponent's hand. 
### The Bot: bot.py
The bot is simply one function that takes in the bots hole cards, any cards that are dealt to the board, and what street the game is on. The function then loads the relevant tensorflow model, predicts the outcome of the hand with the model, and returns the prediction. This is the basis for the bot's play in the game.  

## The Interface





## Results
Overall, the pokerbot was a moderate sucess. On the test data, the models all had an accuracy of between 52 and 55 percent. This is fairly good, considering that a person cannot always tell if they are good. The bot definitely learned some of the basics of poker, like that having higher hole cards is good, and that having more than one of a card value is good. However, more complicated rules, such as having straights or flushes, the bot did not learn. It will often fold a good hand, or predict a win on a good hand. In regards to betting strategy or exploitative play, we did not even attempt this, and is a major factor that could be improved. 

## Installation Instructions
Install the following packages: 
1. Python
2. Numpy
3. Django
4. Tensorflow
5. Keras
6. Sklearn
7. Matplotlib

Run manage.py with the argument "runserver"

Open localhost:8000 and enjoy!