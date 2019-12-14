"""Indiana double deck bid euchre"""
# https://docs.python.org/3/library/random.html#random.shuffle
from random import shuffle

suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
values = ["9", "10", "Jack", "Queen", "King", "Ace"]
names = ["Me", "P1", "Partner", "P2"]

# card class to contain value and suit
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return "{} of {}".format(self.value, self.suit)

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


# deck of cards
class Deck:
    def __init__(self):
        self.cards = []
        for suit in suits:
            for value in values:
                self.cards.append(Card(value, suit))

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        out = ""
        for card in self.cards:
            out += str(card) + "\n"
        return out

    def shuffle(self):
        shuffle(self.cards)

    def dealHand(self, count):
        dealtCards = []
        for i in range(count):
            dealtCards.append(self.cards.pop())
        return dealtCards

    def showKitty(self):
        return self.cards[-1]

    def getKitty(self, discarded):
        kitty = self.cards.pop()
        self.cards.append(discarded)
        return kitty


# player
class Player:
    def __init__(self, name, cards, isDealer):
        self.name = name
        self.cards = cards
        self.isDealer = isDealer

    def get_name(self):
        return self.name

    def get_card(self, index):
        chosenCard = self.cards[index]
        del self.cards[index]
        return chosenCard

    def set_card(self, card):
        self.cards.append(card)

    def is_dealer(self):
        return self.isDealer

    def __str__(self):
        out = self.name + "->\t"
        for i, card in enumerate(self.cards):
            out += str(i + 1) + ": " + str(card) + "\t"
        return out

    def __len__(self):
        return len(self.cards)


def bid_kitty(players):
    trump = ""
    # ask each player if they wish for the dealer to pick the card up
    print("Kitty: " + str(deck.showKitty()))
    for player in players:
        print(player)
        response = input(
            player.get_name()
            + "->\tPress ENTER to pass. Type 'Y' to have dealer pick up card. "
        ).lower()
        # send card to dealers hand and have dealer discard
        if response == "y":
            trump = pickup_trump()
            break
    # begin open bidding
    if trump == "":
        trump = bid_open(deck.showKitty().get_suit())
    return trump


def left_suit():
    if trump == "Hearts":
        return "Diamonds"
    if trump == "Diamonds":
        return "Hearts"
    if trump == "Spades":
        return "Clubs"
    if trump == "Clubs":
        return "Spades"


def left_bower(card):
    return bool(card.get_suit() == left_suit() and card.get_value() == "Jack")


def pickup_trump():
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
    pickup = deck.getKitty(discarded)
    players[3].set_card(pickup)
    print(players[3])
    return pickup.get_suit()


def bid_open(forbiddenSuit):
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
            elif response == "" and player.is_dealer():
                response = ""
            # pass to next player
            elif response == "":
                break
            # invalid input
            else:
                response = ""

            # suit of card turned down from kitty cannot become trump
            if response == forbiddenSuit:
                response = ""
        if response != "":
            trump = response
            break
    return trump


def play_round():
    playedCards = []
    # ask each player to play a card
    for player in players:
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
        played = player.get_card(response)
        playedCards.append(played)
        print(player.get_name() + "->\tPlayed: " + str(played))

    # store first card played
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


# create deck, shuffle
deck = Deck()
deck.shuffle()

# decide dealer and deal cards to players
players = []
dealer = 1
for i, name in enumerate(names):
    if i == dealer:
        players.append(Player("(D)" + name, deck.dealHand(5), True))
    else:
        players.append(Player(name, deck.dealHand(5), False))

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
# trump = bid_kitty(players)
trump = "Hearts"
print("Notice->\tTrump is " + trump)

# play a round
print("Notice->\tRound 1")
play_round()
