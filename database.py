import psycopg2
import os
import dotenv

dotenv.load_dotenv()

connection = psycopg2.connect(os.environ['DATABASE_URI'])

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    id          serial PRIMARY KEY,
    email       varchar(80) UNIQUE NOT NULL,
    password    varchar(80) NOT NULL   -- SHA-1
)"""
CREATE_DECKS_TABLE = """CREATE TABLE IF NOT EXISTS decks (
    id      serial PRIMARY KEY,
    suit    char(1),    -- (D)iamonds, (H)earts, (C)rosses, S(pades)
    value   smallint,   -- 1 for ace, 13 for king.
    deck    int NOT NULL,
    time_drawn float    -- UNIX timestamp when the card has been drawn from deck.
)"""
CREATE_HANDS_TABLE = """CREATE TABLE IF NOT EXISTS hands (
    id      serial PRIMARY KEY,
    time_modified float NOT NULL,
    user_id int,  -- Value of 1 means computer player.
    suit1   char(1),
    value1  smallint,
    suit2   char(1),
    value2  smallint,
    suit3   char(1),
    value3  smallint,
    suit4   char(1),
    value4  smallint,
    suit5   char(1),
    value5  smallint,
    FOREIGN KEY (user_id) REFERENCES users(id))
"""
CREATE_GAME_TABLE_TABLE = """CREATE TABLE IF NOT EXISTS game_table (
    id              serial PRIMARY KEY,
    timestamp_created float NOT NULL,
    computer_hand_id int NOT NULL,
    player_hand_id  int NOT NULL,
    turn_indicator  smallint NOT NULL,  -- Negative means computer's turn. Positive means player's turn.
                                        -- Zero means initial drawing is in progress.
    deck_id         int NOT NULL,
    user_id         int NOT NULL,
    FOREIGN KEY (computer_hand_id) REFERENCES hands(id),
    FOREIGN KEY (player_hand_id) REFERENCES hands(id),
    FOREIGN KEY (deck_id) REFERENCES decks(id),
    FOREIGN KEY (user_id) REFERENCES users(id))"""


def prepare_new_deck():
    """Prepare a new deck to use. Returns int to identify the deck."""
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_DECK_HIGHEST_DECK_IDENTIFIER)
            try:
                deck_id = cursor.fetchone()[0] + 1
            except TypeError:  # If table is empty, fetchone() will return None
                deck_id = 1
            cards = [(suit, value, deck_id) for suit in ("H", "C", "D", "S") for value in range(1, 14)]
            [cursor.execute(INSERT_CARDS_IN_DECKS, card) for card in cards]
            return cursor.fetchone()[0]


CREATE_NEW_USER = r"""INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id AS id;"""
UPDATE_USER = r"""UPDATE users SET email = %s, password = %s WHERE id = %s;"""
GET_DECK_HIGHEST_DECK_IDENTIFIER = r"""SELECT deck FROM decks ORDER BY deck DESC LIMIT 1;"""
INSERT_CARDS_IN_DECKS = r"""INSERT INTO decks (suit, value, deck)
                            VALUES (%s, %s, %s) RETURNING deck;"""
GET_DECK_BY_DECK = """SELECT suit, value, time_drawn FROM decks WHERE deck = %s"""
GET_USER_BY_EMAIL = r"""SELECT * FROM users WHERE email = %s;"""
GET_USER_BY_ID = r"""SELECT * FROM users WHERE id = %s;"""
DRAW_A_CARD = """SELECT id, suit, value, deck
                FROM decks
                WHERE deck = %s AND time_drawn IS NULL
                ORDER BY RANDOM() LIMIT 1;"""
MARK_A_CARD_DRAWN = """UPDATE decks SET time_drawn = (%s) WHERE id = %s;"""
SAVE_HAND = """INSERT INTO hands(suit1, value1, 
                                suit2, value2,
                                suit3, value3,
                                suit4, value4,
                                suit5, value5,
                                timestamp float) -- UNIX timestamp
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
)"""
INSERT_INTO_HANDS = """INSERT INTO hands (suit1, value1, suit2, value2, suit3, value3, suit4, value4, suit5, value5,
                            time_modified, user_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id"""
UPDATE_HAND_TO_HANDS = """UPDATE hands SET suit1 = %s, value1 = %s,
                                            suit2 = %s, value2 = %s,
                                            suit3 = %s, value3 = %s,
                                            suit4 = %s, value4 = %s,
                                            suit5 = %s, value5 = %s,
                                            time_modified = %s
                            WHERE id = %s"""
GET_HAND_BY_ID = """SELECT suit1, value1, suit2, value2, suit3, value3, suit4, value4, suit5, value5,
                            user_id, time_modified FROM hands
                            WHERE id = %s;"""
INSERT_NEW_GAME_TABLE = """INSERT INTO game_table (timestamp_created, computer_hand_id, player_hand_id,
                                                    turn_indicator, deck_id, user_id)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            RETURNING id;"""
UPDATE_GAME_ON_GAME_TABLE = """UPDATE game_table SET computer_hand_id = %s,
                                                    player_hand_id = %s, turn_indicator = %s,
                                                    deck_id = %s, user_id = %s
                                WHERE id=%s"""
# LOAD_A_GAME_BY_ID = """SELECT (game_table.id, game_table.turn_indicator,
#                         users.email,
#                         decks.deck,
#                         -- Player hand and computer hand
#                         hands.suit1, hands.value1, hands.suit2, hands.value2,
#                         hands.suit3, hands.value3, hands.suit4, hands.value4,
#                         hands.suit5, hands.value5, hands.time_modified
#                         ) FROM game_table JOIN users JOIN decks JOIN hands ON
#                                 gametable.user_id = users.id
#                                 AND (gametable.player_hand_id = hands.id
#                                     OR gametable.computer_hand_id = hands.id)
#                         WHERE game_table.id = %s
#                         ORDER BY hands.user_id ASC NULLS LAST"""
GET_LATEST_GAME_TABLE_BY_EMAIL = \
    """SELECT game_table.id, game_table.timestamp_created, game_table.computer_hand_id,
           game_table.player_hand_id, game_table.deck_id, game_table.user_id, turn_indicator
    FROM game_table LEFT JOIN users
    ON game_table.user_id = users.id
    WHERE users.email=%s
    ORDER BY timestamp_created DESC
    LIMIT 1"""


def create_tables():
    import string
    from random import sample
    import exceptions
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_DECKS_TABLE)
            cursor.execute(CREATE_HANDS_TABLE)
            cursor.execute(CREATE_GAME_TABLE_TABLE)
            try:
                chars = string.ascii_letters + string.digits + string.punctuation
                length = 30
                cursor.execute(CREATE_NEW_USER, ("robot@hornantuutti.fi", sample(chars, length)))
            except psycopg2.errors.UniqueViolation as e:
                pass

