from .poker import HeadsUpHand

#*********** creating datasets **********************************
#all functions create a list of hands
# argument n - how many hands to create


#one hand, just for testing purposes
def printAHand():
  hand = HeadsUpHand()
  hand.printHand()

def getTuple(card):
  return card.value, card.suit 

def createHandData(n, street):
    handList = []
    for _ in range(n):
        #get all relevant info
        hand = HeadsUpHand()
        result = hand.heroWins() 
        hero1, hero2 = hand.heroCards
        hero1v, hero1s = getTuple(hero1) 
        hero2v, hero2s = getTuple(hero2)
        board = hand.board
        board1v, board1s = getTuple(board[0])
        board2v, board2s = getTuple(board[1])
        board3v, board3s = getTuple(board[2])
        board4v, board4s = getTuple(board[3])
        board5v, board5s = getTuple(board[4])
        element = None 

        if street == 'preflop':
            element = hero1v, hero1s, hero2v, hero2s, result
        elif street == 'postflop': 
            element = hero1v, hero1s, hero2v, hero2s, board1v, board1s, board2v, board2s, board3v, board3s, result
        elif street == 'turn':
            element = hero1v, hero1s, hero2v, hero2s, board1v, board1s, board2v, board2s, board3v, board3s, board4v, board4s, result
        elif street == 'river':
            element = hero1v, hero1s, hero2v, hero2s, board1v, board1s, board2v, board2s, board3v, board3s, board4v, board4s, board5v, board5s, result
        else:
            return None
        handList.append(element)
    return handList