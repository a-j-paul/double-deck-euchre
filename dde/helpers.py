"""Helper methods"""
"""Indiana double deck bid euchre"""
from random import shuffle
from itertools import cycle
from collections import deque

SUITS = ["Spades", "Clubs", "Hearts", "Diamonds"]
VALUES = ["9", "10", "Jack", "Queen", "King", "Ace"]
PLAYER_NAMES = ["Me", "P1", "Partner", "P2"]
WINNING_SCORE = 52
trump = None
first_suit = None


class Card:
    """
    Cards have suit and value
    """

    def __init__(self, value: str, suit: str):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value} of {self.suit}"

    def __gt__(self, other):
        # left bower trickery
        if trump == "Hearts":
            left = "Diamonds"
        elif trump == "Diamonds":
            left = "Hearts"
        elif trump == "Spades":
            left = "Clubs"
        elif trump == "Clubs":
            left = "Spades"
        else:
            left = None

        if self.suit == left:
            self.suit = trump
            self.value = "Left"
        if other.suit == left:
            other.suit = trump
            other.value = "Left"

        # high and low trump
        if trump == "Low":
            values = ["Ace", "King", "Queen", "Jack", "10", "9"]
            return values.index(self.value) > values.index(other.value)
        if trump == "High":
            values = ["9", "10", "Jack", "Queen", "King", "Ace"]
            return values.index(self.value) > values.index(other.value)

        # if both suits are not trump
        if self.suit != trump and other.suit != trump:
            if self.suit == first_suit and other.suit == first_suit:
                pass
            elif self.suit != first_suit and other.suit != first_suit:
                # TODO: don't think this pass is possible
                pass
            elif self.suit == first_suit and other.suit != first_suit:
                return True
            elif self.suit != first_suit and other.suit == first_suit:
                return False
            values = ["9", "10", "Jack", "Queen", "King", "Ace"]
            return values.index(self.value) > values.index(other.value)
        # if both suits are trump
        elif self.suit == trump and other.suit == trump:
            values = ["9", "10", "Queen", "King", "Ace", "Left", "Jack"]
            return values.index(self.value) > values.index(other.value)
        # if played card is trump and other is not
        elif self.suit == trump and other.suit != trump:
            return True
        # if other card is trump and played card is not
        elif self.suit != trump and other.suit == trump:
            return False

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value


class Deck:
    """
    All cards in 48-card double euchre deck
    """

    def __init__(self):
        self.cards = []
        for i in range(2):
            for suit in SUITS:
                for value in VALUES:
                    self.cards.append(Card(value, suit))

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        out = ""
        for card in self.cards:
            out += str(card) + "\n"
        return out

    def shuffle(self):
        """
        Shuffle the deck of cards
        """
        shuffle(self.cards)

    def deal_hand(self, count: int = 12) -> list:
        """
        Get list of cards from the deck
        """
        dealt_cards = []
        for _i in range(count):
            dealt_cards.append(self.cards.pop())
        return dealt_cards


class Player:
    """
    Player has a hand of cards
    """

    def __init__(self, name: str, cards: list, is_dealer: bool):
        self.name = name
        self.cards = cards
        self.is_dealer = is_dealer

    def get_name(self):
        return self.name

    def get_card(self, index: int) -> Card:
        """
        Remove chosen card from hand
        """
        chosen_card = self.cards[index]
        del self.cards[index]
        return chosen_card

    def set_card(self, card: Card):
        """
        Add card to hand
        """
        self.cards.append(card)

    def set_cards(self, cards: list):
        self.cards = cards

    def sort_cards(self):
        """
        Sort cards according to suit
        """
        # TODO: sort based on current trump setting
        self.cards = sorted(self.cards, key=lambda card: str(card).split("of")[1])

    def __str__(self):
        self.sort_cards()
        out = self.name + "->\t"
        for i, card in enumerate(self.cards):
            out += str(i + 1) + ": " + str(card) + "\t"
        return out

    def __len__(self):
        return len(self.cards)


if __name__ == "__main__":
    # Self is trump and other is not
    trump = "Hearts"
    first_suit = "Hearts"
    c1 = Card("9", "Hearts")
    c2 = Card("10", "Clubs")

    print(f"{trump}\n{c1} > {c2}: {c1>c2}")

    # Both trump + left bower
    trump = "Hearts"
    first_suit = "Hearts"
    c1 = Card("9", "Hearts")
    c2 = Card("Jack", "Diamonds")

    print(f"{trump}\n{c1} > {c2}: {c1>c2}")

    # No trump but followed suit
    trump = "Hearts"
    first_suit = "Clubs"
    c1 = Card("9", "Clubs")
    c2 = Card("Jack", "Spades")

    print(f"{trump}\n{c1} > {c2}: {c1>c2}")

    # Low trump
    trump = "Low"
    first_suit = "Clubs"
    c1 = Card("10", "Clubs")
    c2 = Card("9", "Spades")

    print(f"{trump}\n{c1} > {c2}: {c1>c2}")

    # High trump
    trump = "High"
    first_suit = "Clubs"
    c1 = Card("10", "Clubs")
    c2 = Card("10", "Spades")

    print(f"{trump}\n{c1} > {c2}: {c1>c2}")
