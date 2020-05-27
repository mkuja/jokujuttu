import models.game_table
from models.hand import Hand

from constants import *
import exceptions


class GameTable(models.game_table.GameTable):

    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def hit(self):
        card = self.draw_a_card()
        if self.turn_indicator == PLAYER_TURN_INDICATOR:
            self.player.add_card(card)
        else:
            self.computer.add_card(card)
        self.save()

    def stay(self):
        self.turn_indicator *= -1
        self.save()

    def ask_move(self):
        """Returns the move function computer is going to do."""
        if self.turn_indicator == COMPUTER_TURN_INDICATOR:
            if self.player.hand. # TODO: This is where i got stuck.
        else:
            raise exceptions.Fly("Player's turn, yet ask_move() invoked.")
