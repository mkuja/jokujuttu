
from database import connection
import database

from models.card import Card
from models.deck import Deck
from models.hand import Hand
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
        """Return latest game by a user."""
        with connection:
            with connection.cursor() as cursor:
                user = User.get_user_by_email(email)
                cursor.execute(database.GET_LATEST_GAME_TABLE_BY_EMAIL, (email,))
                (game_table_id, timestamp_created, computer_hand_id,
                 player_hand_id, deck_id, user_id, turn_indicator) = cursor.fetchone()
                # Get Hands
                cursor.execute(database.GET_HAND_BY_ID, (user_id, ))
                player_hand = cursor.fetchone()[0]
                cursor.execute(database.GET_HAND_BY_ID, (computer_hand_id, ))
                computer_hand = cursor.fetchone()[0]
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
