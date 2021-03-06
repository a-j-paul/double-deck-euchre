"""Indiana double deck bid euchre"""
from random import shuffle
from itertools import cycle
from collections import deque

import config

SUITS = ["Spades", "Clubs", "Hearts", "Diamonds"]
VALUES = ["9", "10", "Jack", "Queen", "King", "Ace"]
PLAYER_NAMES = ["Me", "P1", "Partner", "P2"]
WINNING_SCORE = 52


class Card:
    """
    Cards have suit and value
    """

    def __init__(self, value: str, suit: str):
        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.value} of {self.suit}"

    def __gt__(self, other) -> bool:
        # left bower trickery
        if config.trump == "Hearts":
            left = "Diamonds"
        elif config.trump == "Diamonds":
            left = "Hearts"
        elif config.trump == "Spades":
            left = "Clubs"
        elif config.trump == "Clubs":
            left = "Spades"
        else:
            left = None

        if self.suit == left and self.value == "Jack":
            self.suit = config.trump
            self.value = "Left"
        if other.suit == left and self.value == "Jack":
            other.suit = config.trump
            other.value = "Left"

        # high and low config.trump
        if self.suit == config.first_suit and other.suit == config.first_suit:
            if config.trump == "Low":
                values = ["Ace", "King", "Queen", "Jack", "10", "9"]
                return values.index(self.value) > values.index(other.value)
            if config.trump == "High":
                values = ["9", "10", "Jack", "Queen", "King", "Ace"]
                return values.index(self.value) > values.index(other.value)
        elif self.suit != config.first_suit and other.suit != config.first_suit:
            return False
        elif self.suit == config.first_suit and other.suit != config.first_suit:
            return True
        elif self.suit != config.first_suit and other.suit == config.first_suit:
            return False

        # if both suits are not config.trump
        if self.suit != config.trump and other.suit != config.trump:
            if self.suit == config.first_suit and other.suit == config.first_suit:
                pass
            elif self.suit != config.first_suit and other.suit != config.first_suit:
                return False

            elif self.suit == config.first_suit and other.suit != config.first_suit:
                return True
            elif self.suit != config.first_suit and other.suit == config.first_suit:
                return False
            values = ["9", "10", "Jack", "Queen", "King", "Ace"]
            return values.index(self.value) > values.index(other.value)
        # if both suits are config.trump
        elif self.suit == config.trump and other.suit == config.trump:
            values = ["9", "10", "Queen", "King", "Ace", "Left", "Jack"]
            return values.index(self.value) > values.index(other.value)
        # if played card is config.trump and other is not
        elif self.suit == config.trump and other.suit != config.trump:
            return True
        # if other card is config.trump and played card is not
        elif self.suit != config.trump and other.suit == config.trump:
            return False

    def get_suit(self) -> str:
        """ Card suit """
        # left bower trickery
        if config.trump == "Hearts":
            left = "Diamonds"
        elif config.trump == "Diamonds":
            left = "Hearts"
        elif config.trump == "Spades":
            left = "Clubs"
        elif config.trump == "Clubs":
            left = "Spades"
        else:
            left = None

        if self.suit == left and self.value == "Jack":
            return config.trump
        return self.suit

    def get_value(self) -> str:
        """ Card value """
        return self.value


class Deck:
    """
    All cards in 48-card double euchre deck
    """

    def __init__(self):
        self.cards = []
        for _ in range(2):
            for suit in SUITS:
                for value in VALUES:
                    self.cards.append(Card(value, suit))

    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        out = ""
        for card in self.cards:
            out += str(card) + "\n"
        return out

    def shuffle(self) -> None:
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

    def get_name(self) -> str:
        """ Player name """
        return self.name

    def get_card(self, index: int, remove_card: bool = True) -> Card:
        """
        Remove chosen card from hand
        """
        chosen_card = self.cards[index]
        if remove_card:
            del self.cards[index]
        return chosen_card

    def set_card(self, card: Card) -> None:
        """
        Add card to hand
        """
        self.cards.append(card)

    def set_cards(self, cards: list) -> None:
        """ Add multiple cards to hand """
        self.cards = cards

    def sort_cards(self) -> None:
        """
        Sort cards according to suit
        """
        # left bower trickery
        if config.trump == "Hearts":
            left = "Diamonds"
        elif config.trump == "Diamonds":
            left = "Hearts"
        elif config.trump == "Spades":
            left = "Clubs"
        elif config.trump == "Clubs":
            left = "Spades"
        else:
            left = None
        for card in self.cards:
            if card.suit == left and card.value == "Jack":
                card.suit = config.trump
                card.value = "Left"

        def sort_order(card: Card) -> int:
            if card.suit == config.trump:
                values = ["9", "10", "Queen", "King", "Ace", "Left", "Jack"]
            else:
                values = ["9", "10", "Jack", "Queen", "King", "Ace"]

            return values.index(card.value)

        self.cards = sorted(
            self.cards, key=lambda card: (str(card).split("of")[1], sort_order(card))
        )

        # change left name back
        for card in self.cards:
            if card.value == "Left":
                card.suit = left
                card.value = "Jack"

    def __str__(self) -> str:
        self.sort_cards()
        out = self.name + "->\t"
        for i, card in enumerate(self.cards):
            out += str(i + 1) + ": " + str(card) + "\t"
        return out

    def __len__(self) -> int:
        return len(self.cards)


def get_bid() -> dict:
    """
    Get bid from player
    """
    bid = {}

    def check_input(input_string: str):
        # cast value to int
        if input_string.isnumeric():
            input_string = int(input_string)

        return input_string

    bid["value"] = None
    while bid["value"] is None:
        bid["value"] = input(
            "Select bid value (1-12) or type 'pass' to pass or 'alone' to go alone: "
        )
        bid["value"] = check_input(bid["value"])

    # if bid was not passed then get suit
    if bid["value"] != "pass":
        bid["trump"] = input(
            f"Select config.trump suit: high, low, {', '.join(SUITS)}: "
        )
    else:
        bid["trump"] = "pass"

    return bid


def highest_bidder_drops_3_cards(player: Player):
    """
    When going alone the bidder must discard three cards
    """

    def check_inputs(input_string: str) -> list:
        removed_cards = [int(x) for x in input_string.split(",")]
        removed_cards = [x - i - 1 for i, x in enumerate(removed_cards)]
        return removed_cards

    removed_cards = None
    while removed_cards is None:
        removed_cards = input(
            "Type numbers of 3 cards to get rid of separated by commas: "
        )
        removed_cards = check_inputs(removed_cards)

    for removed in removed_cards:
        player.get_card(removed)
    print(player)


def partner_provides_3_cards(partner: Player, bidder: Player):
    """
    When going alone the partern must provide three cards to the bidder
    """

    def check_inputs(input_string: str) -> list:
        removed_cards = [int(x) for x in input_string.split(",")]
        removed_cards = [x - i - 1 for i, x in enumerate(removed_cards)]
        return removed_cards

    removed_cards = None
    while removed_cards is None:
        removed_cards = input(
            "Type numbers of 3 cards to get rid of separated by commas: "
        )
        removed_cards = check_inputs(removed_cards)

    for removed in removed_cards:
        c = partner.get_card(removed)
        bidder.set_card(c)


def play_trick(players, first_player: Player) -> dict:
    """
    Play through one trick
    """
    trick_results = {"Trick Winner": None, "Winning card": None}
    trick_players = players
    trick_players.rotate(trick_players.index(first_player))
    for player in trick_players:
        print(player)
        played = len(player) + 1
        while played > len(player):
            played = input("Type # of card to play: ")
            # handle non-numeric responses
            if not played.isnumeric():
                played = len(player) + 1
            elif int(played) < 1:
                played = len(player) + 1
            else:
                played = int(played)
        played_card = player.get_card(int(played) - 1)
        if (
            trick_results["Winning card"] is None
            or played_card > trick_results["Winning card"]
        ):
            trick_results["Trick Winner"] = player
            trick_results["Winning card"] = played_card

    return trick_results


def update_hand_results(trick_results: dict, hand_results: dict = None) -> dict:
    """
    Track scores after each trick is played
    """
    if hand_results is None:
        hand_results = {}
    hand_results.setdefault("Bidding Team Score", 0)
    hand_results.setdefault("Opposing Team Score", 0)

    if trick_results["Trick Winner"] in config.teams[config.bidding_team]:
        hand_results["Bidding Team Score"] = hand_results["Bidding Team Score"] + 1
    else:
        hand_results["Opposing Team Score"] = hand_results["Opposing Team Score"] + 1
    return hand_results


def play_game():
    """
    Play game
    """
    # setup game
    # build list of players

    players = []
    for player_name in PLAYER_NAMES:
        players.append(Player(player_name, [], False))
    players = deque(players)

    # establish config.teams
    config.teams[1].append(players[0])
    config.teams[1].append(players[2])
    config.teams[2].append(players[1])
    config.teams[2].append(players[3])

    # set team scores to 0
    score = {1: 0, 2: 0}

    # set initial dealer
    players[3].is_dealer = True

    hand_number = 0

    while score[1] < WINNING_SCORE and score[2] < WINNING_SCORE:
        # reshuffle deck
        deck = Deck()
        deck.shuffle()

        # deal hand to each player
        for player in players:
            player.set_cards(deck.deal_hand(12))

        # set dealer to next player in the rotation
        if hand_number > 0:
            players.rotate(1)
            for i in range(3):
                players[i].is_dealer = False
            players[3].is_dealer = True

        # bidding continues until no players wish to make a higher bid
        print("START BIDDING")

        highest_bid = 0
        highest_bid_trump = None
        highest_bidder = None
        pass_count = 0
        alone = False
        for player in cycle(players):
            print(player)
            bid = get_bid()

            # player is not bidding higher
            if bid["value"] == "pass":
                pass_count = pass_count + 1
            # player wishes to shoot the moon/go alone
            elif bid["value"] == "alone":
                highest_bid = 12
                highest_bid_trump = bid["trump"]
                highest_bidder = player
                alone = True
                break
            # new highest bid
            elif bid["value"] > highest_bid:
                highest_bid = bid["value"]
                highest_bid_trump = bid["trump"]
                highest_bidder = player
                pass_count = 0

            # no player wishes to exceed current highest bid, end bidding
            if pass_count == 3:
                break

        # handle card exchange during alone scenario
        if alone:
            partner = players[(players.index(highest_bidder) + 2) % 4]
            highest_bidder_drops_3_cards(highest_bidder)
            partner_provides_3_cards(partner, highest_bidder)

        # track team that made winning bid
        if highest_bidder in config.teams[1]:
            config.bidding_team = 1
            opposing_team = 2
        else:
            config.bidding_team = 2
            opposing_team = 1

        # track winning config.trump
        config.trump = highest_bid_trump
        print(
            f"BIDDING OVER. {highest_bid} {highest_bid_trump} made by {highest_bidder.name}"
        )

        # trick play
        for i in range(12):
            if i == 0:
                trick_results = play_trick(players, highest_bidder)
            else:
                trick_results = play_trick(players, trick_winner)

            trick_winner = trick_results["Trick Winner"]

            # track results of all tricks played so far
            if hand_number > 0:
                hand_results = update_hand_results(trick_results, hand_results)
            else:
                hand_results = update_hand_results(trick_results)

        # update scores
        # bidding team euchred
        if hand_results["Bidding Team Score"] < highest_bid:
            if alone:
                score[config.bidding_team] = score[config.bidding_team] - 24
            else:
                score[config.bidding_team] = score[config.bidding_team] - highest_bid
        # bidding team successful
        else:
            if alone:
                score[config.bidding_team] = score[config.bidding_team] + 24
            else:
                score[config.bidding_team] = (
                    score[config.bidding_team] + hand_results["Bidding Team Score"]
                )
        score[opposing_team] = (
            score[opposing_team] + hand_results["Opposing Team Score"]
        )

        print(score)

        hand_number = hand_number + 1

    print(score)


if __name__ == "__main__":
    play_game()
