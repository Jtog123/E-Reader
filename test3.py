import collections
from random import choice

Card = collections.namedtuple('Card',['rank','suit'])

class FrenchDeck:

    ranks = [str(n) for n in range(2,11)] + list('JKQA')
    suits = "Spades Diamonds Hearts Clubs".split()

    
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]
        
    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]



deck = FrenchDeck()

suit_values = dict(spades = 3, hearts = 2, diamonds = 1, clubs = 0)

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in sorted(deck, key=spades_high):
    print(card)


