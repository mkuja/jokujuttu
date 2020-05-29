from models.game_table import GameTable
from models.user import User

from constants import *
import exceptions


class Game:

    def __init__(self, user: User, new_game=False):
        if new_game:
            self.game_table = GameTable.new_game(user)
            self.draw_two_initial_cards()
        else:
            self.game_table = GameTable.load_latest_game(user.email)

    def hit(self):
        card = self.game_table.draw_a_card()
        if self.game_table.turn_indicator == PLAYER_TURN_INDICATOR:
            self.game_table.player.add_card(card)
        else:
            self.game_table.computer.add_card(card)
        self.game_table.save()

    def stay(self):
        if self.game_table.turn_indicator == PLAYER_TURN_INDICATOR:
            self.game_table.turn_indicator = COMPUTER_TURN_INDICATOR
            self.make_move()
        else:
            self.game_table.turn_indicator = GAME_OVER_TURN_INDICATOR
        self.game_table.save()

    def make_move(self):
        """Returns the move function computer is going to do."""
        if self.game_table.turn_indicator == COMPUTER_TURN_INDICATOR:
            if self.game_table.player.value_of_hand() <= 21\
                    and self.game_table.computer.value_of_hand() <= 17:
                self.hit()
                self.make_move()
            else:
                return self.stay()
        elif self.game_table.turn_indicator == GAME_OVER_TURN_INDICATOR:
            return None
        else:
            raise exceptions.Fly("Player's turn, yet ask_move() invoked.")

    def new_game(self):
        """Return a new game using the same user."""
        return Game(self.game_table.user, new_game=True)

    def get_player_hand(self):
        return self.game_table.player

    def get_computer_hand(self):
        return self.game_table.computer

    def evaluate_winner(self):
        """Return "player" or "computer" or "tie"."""
        if self.game_table.player.is_blackjack() and self.game_table.computer.is_blackjack():
            return "tie"
        elif self.game_table.player.is_blackjack():
            return "player"
        elif self.game_table.computer.is_blackjack():
            return "computer"
        elif self.game_table.player.value_of_hand() > 21:
            return "computer"
        elif self.game_table.computer.value_of_hand() > 21:
            return "player"
        elif self.game_table.computer.value_of_hand() == self.game_table.player.value_of_hand():
            return "tie"
        elif self.game_table.player.value_of_hand() > self.game_table.computer.value_of_hand():
            return "player"
        else:
            return "computer"

    def draw_two_initial_cards(self):
        for i in range(2):
            self.game_table.player.add_card(self.game_table.draw_a_card())
            self.game_table.computer.add_card(self.game_table.draw_a_card())