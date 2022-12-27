from abc import ABC, abstractmethod
from collections import deque
from enum import Enum, IntEnum
from random import shuffle
from secrets import choice
from typing import Deque, List, NamedTuple


class Suit(IntEnum):
    SPADE = 0
    DIAMOND = 13
    HEART = 26
    CLUB = 39

    def __repr__(self) -> str:
        return self.name


class Face(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __repr__(self) -> str:
        return self.name


class Card(NamedTuple):
    suit: Suit
    face: Face

    def id(self):
        return self.suit + self.face


def generate_card_deck() -> List[Card]:
    """Generates a standard 52 card deck"""
    deck = []

    for suit in Suit:
        for face in Face:
            deck.append(Card(suit, face))

    return deck


class Deck(ABC):
    def __init__(self, num_of_decks=1) -> None:
        self.__num_of_decks = num_of_decks

    @abstractmethod
    def draw_card(self) -> Card:
        pass

    def _generate_deck(self) -> List[Card]:
        cards = []
        for _ in range(self.__num_of_decks):
            cards += generate_card_deck()
        return cards


class ContinuousShuffleMachine(Deck):
    def __init__(self, num_of_decks=1) -> None:
        super().__init__(num_of_decks=num_of_decks)


class StandardDeck(Deck):
    def __init__(self, num_of_decks=1) -> None:
        super().__init__(num_of_decks=num_of_decks)
        self.discard_pile: Deque[Card] = deque()
        self.deck: Deque[Card] = deque(self._generate_deck())
        shuffle(self.deck)

    def draw_card(self):
        card = self.deck.popleft()
        self.discard_pile.append(card)
        return card


if __name__ == "__main__":
    from pprint import pprint

    deck = StandardDeck()
    card = deck.draw_card()
    print(card, card.id())
    print(deck.discard_pile)
