import random

class Card:
        def __init__(self, suit, value):
            assert 1<= suit <= 4 and 1 <= value <= 13
            self._suit = suit
            self._value = value

        def getValue(self):
            return self._value
        
        def getSuit(self):
            return self._suit
        
        def __str__(self):
            card_type = {1:"Hearts", 2:"Diamonds", 3:"Clubs",4 :"Spades"}
            card_number = {1:"Ace", 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:"Joker", 12:"Queen", 13:"king"}
            return(f"{card_number[self.getValue()]} of {card_type[self.getSuit()]}") 
        

#my_card = Card(4,11)
#print(my_card)
            

class CardDeck:
     def __init__(self):
          self.card_deck = []
          self.reset()
          
     def shuffle(self):
          random.shuffle(self.card_deck)
        
     def getCard(self):
        return self.card_deck.pop()

     def size(self):
        return self.card_deck.__len__()
     
     def reset(self):
        self.card_deck.clear()
        for x in range(1,5):
               for y in range(1,14):
                    card = Card(x,y)
                    self.card_deck.append(card)

     
deck = CardDeck()
deck.shuffle()
while deck.size() > 0:
     Card = deck.getCard()
     print("Card {} has value {}" . format(Card, Card.getValue()))
