from models.game_table import GameTable
from models.user import User

from constants import *
import exceptions


class Game:

    def __init(self, user: User):
        self.game_table = GameTable.load_latest_game(user.email)

    def hit(self):
        card = self.draw_a_card()
        if self.game_table.turn_indicator == PLAYER_TURN_INDICATOR:
            self.game_table.player.add_card(card)
        else:
            self.game_table.computer.add_card(card)
        self.game_table.save()

    def stay(self):
        if self.game_table.turn_indicator == PLAYER_TURN_INDICATOR:
            self.game_table.turn_indicator = COMPUTER_TURN_INDICATOR
        else:
            self.game_table.turn_indicator = GAME_OVER_TURN_INDICATOR
        self.game_table.save()

    def ask_move(self):
        """Returns the move function computer is going to do."""
        if self.game_table.turn_indicator == COMPUTER_TURN_INDICATOR:
            if self.game_table.player.value_of_hand() <= 21\
                    and self.game_table.computer.value_of_hand() <= 17:
                return self.hit
            else:
                return self.stay
        else:
            raise exceptions.Fly("Player's turn, yet ask_move() invoked.")
