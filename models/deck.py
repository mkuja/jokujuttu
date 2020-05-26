from database import connection
import database
from models.card import Card
import datetime

class Deck:
    def __init__(self, id=None):
        self.id = id
        if not self.id:
            self.id = database.prepare_new_deck()

    def __repr__(self):
        return f"User({self.id!r})"

    def draw(self):
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(database.DRAW_A_CARD, (self.id,))
                _id, suit, value, deck = cursor.fetchone()
                cursor.execute(database.MARK_A_CARD_DRAWN, (datetime.datetime.timestamp(datetime.datetime.now()), _id))
                return Card(suit, value)