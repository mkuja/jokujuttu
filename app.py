import database
database.create_tables()

import argparse

parser = argparse.ArgumentParser(description="Play some blackjack.")
parser.add_argument("--textui", action="store_true")

args = parser.parse_args()
