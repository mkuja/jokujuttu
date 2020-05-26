
from models.card import Card
from models.user import User
from database import connection
import database
import datetime
from typing import Tuple
from itertools import tee


class Hand:

    def __init__(self, user: User, *cards: Card):
        """cards must be provided as type Card."""
        self.id = None
        self.user = user
        self.cards = []
        if cards:
            self.cards += list(cards)
        self.save()

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
                (suit1, value1, suit2, value2, suit3, value3, suit4, value4, suit5, value5,
                 user_id, time_modified) = cursor.fetchone()
                cards = []
                for suit, value in Hand.pairwise(
                        (suit1, value1, suit2, value2, suit3, value3, suit4, value4, suit5, value5)):
                    if suit and value:
                        cards.append(Card(suit, value))
                return cls(User.get_user_by_id(user_id), *cards)

    @staticmethod
    def pairwise(iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)
