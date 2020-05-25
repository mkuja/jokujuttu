
class WrongPassword(Exception):
    """Raised when trying to INSERT a user into the DB with email that already exists."""
    pass


class UserNotFound(Exception):
    """Raised when trying to look up a user, but one is not found."""
    pass

class Error(Exception):
    """Meant to be subclassed. An unrecoverable error has occurred."""
    pass

class NotImplementedError(Error):
    """This feature is supposed to be implemented by a subclass."""
    pass

class LoadingError(Error):
    """Happens when something is pooped when trying to load things."""

    def __init__(self, *args, **kwargs):
        super(self, *args, **kwargs)