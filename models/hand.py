
from models.card import Card
from models.user import User
from database import connection
import database
import datetime
from typing import Tuple


class Hand:

    def __init__(self, user: User, cards=None):
        """cards must be provided as type Card."""
        self.id = None
        self.user = user
        self.cards = []
        if cards:
            self.cards += list(cards)

    def __repr__(self):
        return f"Hand({self.user!r}, {tuple(self.cards)!r})"

    def add_card(self, card: Card):
        self.cards.append(card)

    def get_cards(self) -> Tuple[Card]:
        return tuple(self.cards)

    def save(self):
        # hand = tuple([element for tpl in self.cards for element in tpl])
        hand = tuple([element for tpl in self.cards for element in (tpl.suit, tpl.value)])
        hand += (None,) * (10 - len(hand))
        hand += (datetime.datetime.timestamp(datetime.datetime.now()),)
        print(hand)
        with connection:
            with connection.cursor() as cursor:
                if not self.id:
                    # Omits self.id. Inserts link to the owner of the hand.
                    cursor.execute(database.INSERT_INTO_HANDS, hand + (self.user.id, ))
                    self.id = cursor.fetchone()[0]
                else:
                    # Owner already exists on the table.
                    cursor.execute(database.UPDATE_HAND_TO_HANDS, hand + (self.id,))

    @classmethod
    def load(cls, id):
        """id in the hands table."""
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(database.GET_HAND_BY_ID, (id, ))