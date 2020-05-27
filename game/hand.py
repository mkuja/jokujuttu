
import models.hand


class Hand(models.hand.Hand):

    def value_of_hand(self):
        value = 0
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

