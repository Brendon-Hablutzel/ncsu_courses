from enum import Enum


class Session(Enum):
    Spring = "1"
    Summer1 = "6"
    Summer2 = "7"
    Fall = "8"


class Term:
    """
    Represents a term (which is a two-digit year and a session).
    """

    def __init__(self, year: int, session: Session):
        """
        Creates a new term, given a two-digit year (ex. 24 for 2024) and a session
        (such as spring or fall).
        """
        self.year = year
        self.session = session

    def get_term_number(self) -> int:
        """
        The courses API requires an integer representing the term. This function
        generates that integer using the values passed to the associated Term
        object.
        """
        return int("2" + str(self.year) + self.session.value)
