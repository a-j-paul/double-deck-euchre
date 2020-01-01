"""Indiana double deck bid euchre"""
# https://docs.python.org/3/library/random.html#random.shuffle
from random import shuffle

SUITS = ["Spades", "Clubs", "Hearts", "Diamonds"]
VALUES = ["9", "10", "Jack", "Queen", "King", "Ace"]
names = ["Me", "P1", "Partner", "P2"]


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
        # if suit is not trump
        if self.suit != trump:
            values = ["9", "10", "Jack", "Queen", "King", "Ace"]
            return values.index(self.value) > values.index(other.value)
        # if suit is trump
        elif self.suit == trump:
            values = ["9", "10", "Queen", "King", "Ace", "Jack"]
            return values.index(self.value) > values.index(other.value)

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value


class Deck:
    """
    All cards in 24-card euchre deck
    """

    def __init__(self):
        self.cards = []
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

    def deal_hand(self, count: int) -> list:
        """
        Get list of cards from the deck
        """
        dealt_cards = []
        for _i in range(count):
            dealt_cards.append(self.cards.pop())
        return dealt_cards

    def show_kitty(self) -> Card:
        """
        Return face-up card in the kitty
        """
        return self.cards[-1]

    def get_kitty(self, discarded: Card) -> Card:
        """
        Exchange face-up card in kitty with discarded card
        """
        kitty = self.cards.pop()
        self.cards.append(discarded)
        return kitty


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

    def dealer(self):
        return self.is_dealer

    def sort_cards(self):
        """
        Sort cards according to suit
        """
        self.cards = sorted(self.cards, key=lambda card: str(card).split("of")[1])

    def get_current_suits(self) -> dict:
        """
        Return the quantity of each suit in a player's hand
        """
        # create data structure
        current_suits = {suit: 0 for suit in SUITS}

        for card in self.cards:
            s = card.get_suit()
            if left_bower(card):
                s = trump
            current_suits[s] = current_suits[s] + 1
        return current_suits

    def __str__(self):
        self.sort_cards()
        out = self.name + "->\t"
        for i, card in enumerate(self.cards):
            out += str(i + 1) + ": " + str(card) + "\t"
        return out

    def __len__(self):
        return len(self.cards)


def bid_kitty(players: list) -> str:
    """
    Establish trump suit through kitty or open bidding
    """
    trump = ""
    # ask each player if they wish for the dealer to pick the card up
    print("Kitty: " + str(deck.show_kitty()))
    for player in players:
        print(player)
        response = input(
            player.get_name()
            + "->\tPress ENTER to pass. Type 'Y' to have dealer pick up card. "
        ).lower()
        # send card to dealers hand and have dealer discard
        if response == "y":
            trump = pickup_trump()
            trump_picker = player.get_name()
            break
    # begin open bidding
    if trump == "":
        trump, trump_picker = bid_open(deck.show_kitty().get_suit())
    return trump, trump_picker


def left_suit() -> str:
    """
    Return suit of the left bower
    """
    if trump == "Hearts":
        return "Diamonds"
    if trump == "Diamonds":
        return "Hearts"
    if trump == "Spades":
        return "Clubs"
    if trump == "Clubs":
        return "Spades"


def left_bower(card: Card) -> bool:
    """
    Check if card is the left bower
    """
    return bool(card.get_suit() == left_suit() and card.get_value() == "Jack")


def pickup_trump() -> str:
    """
    Have dealer pick up face-up kitty card and discard one of their cards
    """
    # hard coded to player 3
    print(players[3])
    response = -1
    while response >= len(players[3]) or response < 0:
        response = (
            int(
                input(
                    players[3].get_name()
                    + "->\tWhich card #1-5 do you want to discard? "
                )
            )
            - 1
        )
    discarded = players[3].get_card(response)
    pickup = deck.get_kitty(discarded)
    players[3].set_card(pickup)
    print(players[3])
    return pickup.get_suit()


def bid_open(forbidden_suit: str) -> str:
    """
    Open bidding to establish trump suit. Suit of card on top of kitty that was rejected cannot be picked.
    """
    # ask each player if they wish to declare trump
    for player in players:
        print(player)
        response = ""
        while response == "":
            response = input(
                player.get_name()
                + "->\tPress ENTER to pass. Otherwise, which suit do you want to declare as trump? "
            ).lower()
            if "heart" in response:
                response = "Hearts"
            elif "spade" in response:
                response = "Spades"
            elif "club" in response:
                response = "Clubs"
            elif "diamond" in response:
                response = "Diamonds"
            # dealer must declare suit if all other players have passed
            elif response == "" and player.dealer():
                response = ""
            # pass to next player
            elif response == "":
                break
            # invalid input
            else:
                response = ""

            # suit of card turned down from kitty cannot become trump
            if response == forbidden_suit:
                response = ""
        if response != "":
            trump = response
            trump_picker = player.get_name()
            break
    return trump, trump_picker


def play_trick() -> int:
    """
    Play through one trick
    """
    playedCards = []
    # ask each player to play a card
    for i, player in enumerate(players):
        print(player)
        response = -1
        while response >= len(player) or response < 0:
            response = (
                int(
                    input(
                        player.get_name()
                        + "->\tWhich card #1-"
                        + str(len(player))
                        + " do you want to play? "
                    )
                )
                - 1
            )
            # check card for renege
            if i > 0:
                current_suits = player.get_current_suits()
                # if player has card(s) matching the suit of the first card played
                # then they must follow suit
                if current_suits[suit] > 0:
                    # remove card from hand to check suit
                    try:
                        played = player.get_card(response)
                    except IndexError:
                        response = -1
                    else:
                        if played.get_suit() != suit:
                            response = -1
                        # put card back in hand
                        player.set_card(played)
                        player.sort_cards()

        played = player.get_card(response)
        playedCards.append(played)
        print(player.get_name() + "->\tPlayed: " + str(played))

        # store first card played
        if i == 0:
            winning = playedCards[0]
            winningPlayer = 0
            suit = playedCards[0].get_suit()
            isLeft = left_bower(playedCards[0])
            isWinningTrump = bool(suit == trump or isLeft)

    # find winning card of the round
    for i, card in enumerate(playedCards):
        isLeft = left_bower(card)
        isTrump = bool(card.get_suit() == trump or isLeft)
        # if card followed suit, is not trump, and there was not already trump played
        if (
            card.get_suit() == suit
            and card.get_suit() != trump
            and not isLeft
            and not isWinningTrump
        ):
            if card > winning:
                winning = card
                winningPlayer = i
        # if card followed suit and is trump
        if card.get_suit() == suit and isTrump:
            if isLeft and not winning.get_value() == "Jack":
                winning = card
                winningPlayer = i
            elif card > winning:
                winning = card
                winningPlayer = i
        # if card did not follow suit, is trump, and there was not already trump played
        if card.get_suit() != suit and isTrump and not isWinningTrump:
            winning = card
            winningPlayer = i
            isWinningTrump = True
        # if card did not follow suit, is trump, and there was already trump played
        if card.get_suit() != suit and isTrump and isWinningTrump:
            if isLeft and not winning.get_value() == "Jack":
                winning = card
                winningPlayer = i
            elif card > winning:
                winning = card
                winningPlayer = i

    winner = players[winningPlayer].get_name()
    print("Notice->\tWinning card is " + str(winning) + " by player " + winner)
    return winningPlayer


if __name__ == "__main__":
    # create deck, shuffle
    deck = Deck()
    deck.shuffle()

    # decide dealer and deal cards to players
    players = []
    dealer = 1
    for i, name in enumerate(names):
        if i == dealer:
            players.append(Player("(D)" + name, deck.deal_hand(5), True))
        else:
            players.append(Player(name, deck.deal_hand(5), False))

    # if dealer is not already last in list of players then move them to end
    if dealer != 3:
        move = 3 - dealer
        movedPlayers = []
        for i in range(move):
            movedPlayers.append(players.pop())
        movedPlayers.reverse()
        for i in range(move):
            players.insert(0, movedPlayers.pop())

    # set trump suit
    print("Notice->\tNaming Trump")
    trump, trump_picker = bid_kitty(players)
    print("Notice->\tTrump is " + trump)

    # play a hand
    hand_score = {"Me": 0, "Computer": 0}
    for i in range(1, 6):
        print(f"Notice->\tTrick {i}")
        winner = play_trick()

        # TODO: reorder sequence of players based upon winner
        if winner % 2 == 0:
            hand_score["Me"] = hand_score["Me"] + 1
        else:
            hand_score["Computer"] = hand_score["Computer"] + 1

    # TODO: score after all tricks are over
    # TODO: add loner

    # if trump picker score < 3
    # other team score + 2

    # if trump picker score >= 3 and < 5
    # trump picker score + 1

    # if trump picker score == 5 and loner
    # trump picker score + 4

    # if trump picker score == 5
    # trump picker score + 2
