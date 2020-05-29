
class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"Card({self.suit!r}, {self.value!r})"

    def __str__(self):
        return f"{self.suit + str(self.value)}"
