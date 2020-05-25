import unittest

from database import connection
import database
from models.user import User
from models.card import Card
from models.deck import Deck
# from models.player import Player
from models.hand import Hand


class TestUser(unittest.TestCase):
    def test_save(self):
        username = "m.kujala@live.com"
        password = "password"
        try:
            user = User.get_user_by_email(username, password)
        except Exception as e:
            user = User(username, password)
        user.save()
        deck = Deck()
        hand = Hand(user)
        hand.add_card(deck.draw())
        hand.add_card(deck.draw())
        hand.add_card(deck.draw())
        hand.save()



if __name__ == '__main__':
    unittest.main()
