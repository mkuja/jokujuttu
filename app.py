# TODO: -- Don't allow user to draw cards for the computer using draw() after staying.
# TODO: Make a sane reply from API in the case above.

# TODO: Prevent logging in with empty email.

import database

import argparse

from game.game import Game
from models.user import User
from game.hand import Hand
from exceptions import *

from api.api import app

database.create_tables()


parser = argparse.ArgumentParser(description="Play some blackjack.")
parser.add_argument("--textui", action="store_true")

args = parser.parse_args()

def print_menu():
    print("-------")
    print('l) Lisää yksi kortti.')
    print("j) Jätä tähän.")
    print("t) Tulosta kädet.")
    print("u) Uusi peli.")
    print("q) Lopeta")

if __name__ == "__main__":

    if args.textui:
        try:
            user = User("test@user.fi", "password")
        except EmailAlreadyRegistered as e:
            user = User.get_user_by_email("test@user.fi")
        game = Game(user)
        print_menu()
        while(input_ := input(": ")) != "q":
            if input_ == "l":
                game.hit()
            elif input_ == "j":
                game.stay()
                winner = game.evaluate_winner()
                if winner == "tie":
                    print("Game is a tie!")
                else:
                    print("Player wins!") if game.evaluate_winner() == "player" else print("Computer wins!")
            elif input_ == "t":
                print(f"User: {game.get_player_hand()}\nComputer: {game.get_computer_hand()}\n")
            elif input_ == "u":
                game = game.new_game()
            print_menu()
    else:
        app.run(debug=True)

