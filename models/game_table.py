
from database import connection
import database

from models.card import Card
from models.deck import Deck
from models.hand import Hand
from models.user import User

from exceptions import NotImplementedError

class GameTable:

    def __init__(self, deck: Deck, user: User, player: Hand, computer: Hand):
        self.deck = deck
        self.user = user
        self.player = player
        self.computer = computer

    @classmethod
    def load(cls, id_):
        """Load gametable with id from the database."""
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(database.LOAD_A_GAME, (id_, ))

    def game_situation(self):
        """Return player and computer hands, whose turn it is."""
        pass

    def draw_a_card(self):
        """Draw a card, either for player or computer, if there is a card to be drawn."""
        raise NotImplementedError("Override draw_a_card(), please.")

    def stay(self):
        """Stays either player or computer, depending on whose turn it is."""
        pass

