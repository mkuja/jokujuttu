
import models.hand


class Hand(models.hand.Hand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        self.filter_cards()
        ret = ""
        for card in self.cards:
            ret += f"{card}, "
        return ret[:-2] + " = " + str(self.value_of_hand())

    def value_of_hand(self):
        value = 0
        self.filter_cards()
        for card in self.get_cards():
            if card.value == 1:
                value += 11 if value + 11 <= 21 else 1
            elif card.value == 11 or card.value == 12 or card.value == 13:
                value += 10
            else:
                value += card.value
        return value

    def is_blackjack(self):
        cond1 = self.value_of_hand() == 21 and len(self) == 2
        cond2 = len(self) == 5 and self.value_of_hand() <= 21
        return True if cond1 or cond2 else False

    def filter_cards(self):
        """A small utility to rid of None cards."""
        self.cards = [card for card in self.cards if card.suit and card.value]
