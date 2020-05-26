
from database import connection
import database

from models.card import Card
from models.deck import Deck
from models.hand import Hand
from models.user import User

from exceptions import NotImplementedError

from datetime import datetime


class GameTable:
    """All game actions happen on GameTable, and this GameTable takes care of database interactions.

    This class is inherited by game.game_table.GameTable, which contains game logic.

    Instead of using the constructor, it is recommended to use new_game() classmethod, which initializes all other
    objects needed for a game, aswell as saves everything to the database.
    """

    def __init__(self, deck: Deck, user: User, player: Hand, computer: Hand, id_: int, turn_indicator: int):
        """Classmethod new_game() takes fewer arguments and saves everything to the database."""
        self.deck = deck
        self.user = user
        self.player = player
        self.computer = computer
        self.turn_indicator = turn_indicator
        self.id = id_

    @classmethod
    def new_game(cls, user: User):
        deck = Deck()
        player_hand = Hand(user)
        computer_hand = Hand(User.get_user_by_id(1))  # 1 is the ID of the computer player.
        timestamp = datetime.timestamp(datetime.now())
        with connection:
            with connection.cursor() as cursor:
                # 1 here and at the return statement is turn_indicator. 1 Means player's turn.
                cursor.execute(database.INSERT_NEW_GAME_TABLE, (timestamp, computer_hand.id, player_hand.id,
                                                                1, deck.id, user.id))
                id_ = cursor.fetchone()[0]
        return GameTable(deck, user, player_hand, computer_hand, id_, 1)

    @classmethod
    def load_latest_game(cls, email):
        """Return latest game by a user."""
        with connection:
            with connection.cursor() as cursor:
                user = User.get_user_by_email(email)
                cursor.execute(database.GET_NEWEST_GAME_BY_USER_EMAIL, (email,))
                for party in ("player", "computer"):
                    (id_, turn_indicator, email, deck_number, suit1, value1, suit2, value2, suit3, value3,
                     suit4, value4, suit5, value5, time_modified) = cursor.fetchone()
                    hand = Hand(user, Card(suit1, value1), Card(suit2, value2), Card(suit3, value3), Card(suit4, value4)
                                , Card(suit5, value5))
                    if party == "player":
                        player_hand = hand
                    else:
                        computer_hand = hand

                deck = Deck(deck_number)
                return cls(deck, user, player_hand, computer_hand, id_, turn_indicator)

    def get_id(self):
        return self.id

    def game_situation(self):
        """Return player and computer hands, whose turn it is."""
        pass

    def draw_a_card(self):
        """Draw a card, either for player or computer, if there is a card to be drawn."""
        return self.deck.draw()
    def stay(self):
        """Stays either player or computer, depending on whose turn it is."""
        pass

