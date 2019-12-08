class Card:
    """
    Playing card
    """

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"


my_card = Card("Hearts", "9")
print(my_card)
