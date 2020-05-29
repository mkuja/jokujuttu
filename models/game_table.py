from constants import COMPUTER_UID
from database import connection
import database

from models.card import Card
from models.deck import Deck
#from models.hand import Hand
from game.hand import Hand
from models.user import User
import constants

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
                                                                constants.PLAYER_TURN_INDICATOR, deck.id, user.id))
                id_ = cursor.fetchone()[0]
        return GameTable(deck, user, player_hand, computer_hand, id_, constants.PLAYER_TURN_INDICATOR)

    @classmethod
    def load_latest_game(cls, email):
        """Return latest game by a user or a new game if one didn't exist."""
        with connection:
            with connection.cursor() as cursor:
                user = User.get_user_by_email(email)
                cursor.execute(database.GET_LATEST_GAME_TABLE_BY_EMAIL, (email,))
                bulk = cursor.fetchone()
                print (bulk)
                if bulk:
                    (game_table_id, timestamp_created, computer_hand_id,
                     player_hand_id, deck_id, user_id, turn_indicator) = bulk
                else:
                    return cls.new_game(user)
                # Get Hands
                cursor.execute(database.GET_HAND_BY_ID, (player_hand_id, ))
                p_s1, p_v1, p_s2, p_v2, p_s3, p_v3, p_s4, p_v4, p_s5, p_v5,\
                    uid, mtime = cursor.fetchone()
                player = User.get_user_by_id(uid)
                player_hand = Hand(player, Card(p_s1, p_v1),
                                   Card(p_s2, p_v2),
                                   Card(p_s3, p_v3),
                                   Card(p_s4, p_v4),
                                   Card(p_s5, p_v5))
                cursor.execute(database.GET_HAND_BY_ID, (computer_hand_id, ))
                c_s1, c_v1, c_s2, c_v2, c_s3, c_v3, c_s4, c_v4, c_s5, c_v5,\
                    cuid, cmtime = cursor.fetchone()
                computer = User.get_user_by_id(COMPUTER_UID)
                computer_hand = Hand(computer, Card(c_s1, c_v1),
                                     Card(c_s2, c_v2),
                                     Card(c_s3, c_v3),
                                     Card(c_s4, c_v4),
                                     Card(c_s5, c_v5))
                deck = Deck(deck_id)
                return cls(deck, user, player_hand, computer_hand, game_table_id, turn_indicator)

    def save(self):  # TODO: Check that the thing actually exists in the database.
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(database.UPDATE_GAME_ON_GAME_TABLE, (self.computer.id, self.player.id,
                                                                    self.turn_indicator,
                                                                    self.deck.id, self.user.id,
                                                                    self.id))

    def get_id(self):
        return self.id

    def draw_a_card(self) -> Card:
        """Draw a card, either for player or computer, depending on self.turn_indicator."""
        return self.deck.draw()

    def stay(self):
        """Stays either player or computer, depending on whose turn it is.

        Only player needs to invoke this."""
        self.turn_indicator = constants.COMPUTER_TURN_INDICATOR
        self.save()
