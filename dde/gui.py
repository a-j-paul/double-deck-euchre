""" GUI for double deck euchre """
from euchre import *

import tkinter as tk

import config


class Euchre_GUI:
    def __init__(self, master):
        self.master = master
        master.title("Double Deck Euchre")

        # setup game
        # build list of players
        self.players = []
        for player_name in PLAYER_NAMES:
            self.players.append(Player(player_name, [], False))
        self.players = deque(self.players)

        # establish teams
        config.teams[1].append(self.players[0])
        config.teams[1].append(self.players[2])
        config.teams[2].append(self.players[1])
        config.teams[2].append(self.players[3])

        # set team scores to 0
        score = {1: 0, 2: 0}

        # set initial dealer
        self.players[3].is_dealer = True

        hand_number = 0

        # reshuffle deck
        deck = Deck()
        deck.shuffle()

        # deal hand to each player
        for player in self.players:
            player.set_cards(deck.deal_hand(12))

        # set dealer to next player in the rotation
        if hand_number > 0:
            self.players.rotate(1)
            for i in range(3):
                self.players[i].is_dealer = False
            self.players[3].is_dealer = True

        # bidding continues until no players wish to make a higher bid
        print("START BIDDING")

        highest_bid = 0
        highest_bid_trump = None
        highest_bidder = None
        pass_count = 0
        alone = False
        self.player_num = 0

        config.trump = "Hearts"
        self.card_btns = self.setup_cards()
        self.show_hand(self.player_num)

        lbl_trump = tk.Label(master=master, text=f"Trump: {config.trump}")
        lbl_trump.grid(row=3, column=0)

        btn_next_player = tk.Button(
            master=master, text="Next Player", command=self.next_player
        )
        btn_next_player.grid(row=4, column=0)

    def next_player(self):
        self.player_num = (self.player_num + 1) % 4
        self.show_hand(self.player_num)

    def pick_card(self, btn):
        print(btn["text"])

    def setup_cards(self):
        btns = []

        for i in range(2):
            self.master.columnconfigure(i, weight=1, minsize=75)
            self.master.rowconfigure(i, weight=1, minsize=50)

            for j in range(0, 6):
                frame = tk.Frame(master=self.master, relief=tk.RAISED, borderwidth=1,)
                frame.grid(row=i, column=j, padx=5, pady=5)

                button = tk.Button(master=frame, text="",)
                button.pack(padx=5, pady=5)
                button.configure(command=lambda btn=button: self.pick_card(btn))

                btns.append((frame, button))

        return btns

    def show_hand(self, player_num):
        """
        for i in range(2):
            self.master.columnconfigure(i, weight=1, minsize=75)
            self.master.rowconfigure(i, weight=1, minsize=50)

            for j in range(0, 6):
                converter = lambda x: "dark green" if x == config.trump else "yellow"
                frame = tk.Frame(
                    master=self.master,
                    relief=tk.RAISED,
                    borderwidth=1,
                    bg=converter(
                        self.players[player_num].get_card(i * 2 + j, False).get_suit()
                    ),
                )
                frame.grid(row=i, column=j, padx=5, pady=5)

                button = tk.Button(
                    master=frame,
                    text=f"{self.players[player_num].get_card(i*2+j, False)}",
                )
                button.pack(padx=5, pady=5)
                button.configure(command=lambda btn=button: self.pick_card(btn))
        """
        for i, (frame, btn) in enumerate(self.card_btns):
            converter = lambda x: "dark green" if x == config.trump else "yellow"
            frame.configure(
                bg=converter(self.players[player_num].get_card(i, False).get_suit())
            )
            btn.configure(text=f"{self.players[player_num].get_card(i, False)}")


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = Euchre_GUI(root)
    root.mainloop()
