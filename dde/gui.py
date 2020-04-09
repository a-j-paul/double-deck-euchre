""" GUI for double deck euchre """
from euchre import *

import tkinter as tk

import config


class Euchre_GUI:
    def __init__(self, master):
        self.master = master
        master.title("Double Deck Euchre")
        config.trump = "Hearts"
        deck = Deck()
        deck.shuffle()
        p1 = Player("Player 1", [], False)
        p1.set_cards(deck.deal_hand(12))
        p1.sort_cards()

        for i in range(3):
            master.columnconfigure(i, weight=1, minsize=75)
            master.rowconfigure(i, weight=1, minsize=50)

            for j in range(0, 4):
                converter = lambda x: "dark green" if x == config.trump else "yellow"
                frame = tk.Frame(
                    master=master,
                    relief=tk.RAISED,
                    borderwidth=1,
                    bg=converter(p1.get_card(0, False).get_suit()),
                )
                frame.grid(row=i, column=j, padx=5, pady=5)

                label = tk.Label(master=frame, text=f"{p1.get_card(0)}")
                label.pack(padx=5, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = Euchre_GUI(root)
    root.mainloop()
