from itertools import product
from random import shuffle

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Deck(metaclass=SingletonMeta):
    def __init__(self):
        Suits = ["\u2663", "\u2665",
                 "\u2666", "\u2660"]
        # a list of all the ranks
        Ranks = ['A', '2', '3', '4', '5',
                 '6', '7', '8', '9', '10',
                 'J', 'Q', 'K']
        self.points = {'A': (1, 11), '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10,
                       'Q': 10, 'K': 10}
        self.cards = list(product(Ranks, Suits))
        shuffle(self.cards)

    def deal_cards(self, num_cards):
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

    def get_deck(self):
        deck_str = [f"[{rank}{suit}]" for rank, suit in self.cards]
        return ' '.join(deck_str)

