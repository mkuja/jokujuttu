from database import connection
import database

from exceptions import *


class User:
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self.id = _id

    def __repr__(self):
        return f"User({self.email!r}, {self.password!r}, {self.id!r})"

    def save(self):
        if not self.id:  # Insert a new one in to the database.
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(database.CREATE_NEW_USER, (self.email, self.password))
                    self.id = cursor.fetchone()[0]
        else:  # Update an old record. TODO: Fix updating password in this way.
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(database.UPDATE_USER, (self.email, self.password, self.id))

    @classmethod
    def get_user_by_email(cls, email, password) -> "User":
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(database.GET_USER_BY_EMAIL, (email,))
                id_, email, pw_from_db = cursor.fetchone()
                print(id_, email, pw_from_db)
                if id_:
                    if password == pw_from_db:
                        return cls(email, password, id_)
                    else:
                        raise WrongPassword("Wrong password.")
                else:
                    raise UserNotFound("User not found.")