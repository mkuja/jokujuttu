from database import connection
import database
import psycopg2

from exceptions import *


class User:
    def __init__(self, email, password=None, _id=None):
        self.email = email
        self.password = password
        self.id = _id
        if not self.id:
            self.save()

    def __repr__(self):
        return f"User({self.email!r}, {self.password!r}, {self.id!r})"

    def save(self):
        """Raises EmailAlreadyRegistered exception if it is so."""
        if not self.id:  # Insert a new one in to the database.
            with connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(database.CREATE_NEW_USER, (self.email, self.password))
                        self.id = cursor.fetchone()[0]
                    except psycopg2.errors.UniqueViolation:
                        raise EmailAlreadyRegistered("Try another email address.")

    @classmethod
    def get_user_by_email(cls, email) -> "User":
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(database.GET_USER_BY_EMAIL, (email,))
                try:
                    id_, email, pw_from_db = cursor.fetchone()
                except TypeError:
                    id_ = None
                if id_:
                    return cls(email, pw_from_db, id_)
                else:
                    raise UserNotFound("User not found.")

    @classmethod
    def get_user_by_id(cls, id_):
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(database.GET_USER_BY_ID, (id_,))
                try:
                    id_, email, pw_from_db = cursor.fetchone()
                except TypeError:
                    id_ = None
                if id_:
                    return cls(email, pw_from_db, id_)
                else:
                    raise UserNotFound("User not found.")
