import unittest

from database import connection
import database
from models.user import User
from models.game_table import GameTable
from models.card import Card
from models.deck import Deck
# from models.player import Player
from models.hand import Hand
import exceptions
from game import game


class TestUser(unittest.TestCase):
    def test_save(self):
        username = "m.kujala@live.com"
        password = "password"
        try:
            user = User.get_user_by_email(username)
        except exceptions.UserNotFound:
            user = User(username, password)
            user.save()
        game = game.GameTable.new_game(user)
        game.draw_a_card()
        game.draw_a_card()
        game.stay()
        game.draw_a_card()
        game.draw_a_card()


if __name__ == '__main__':
    unittest.main()
