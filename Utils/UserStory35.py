from datetime import datetime
from Utils.Utils import is_n_days_after


def born_within_thirty_days(person, from_date=datetime.today()):
    """
    Check if a user was born within 30 days of the given datetime
    Note: For the datetime of June 15th, 2000, the value of May 20th, 2000 is true, but May 20th, 1999 is False
    Function is declared static as it does not make use of self
    :param person: The person to check again, must have the BIRT field
    :param from_date: The datetime to check from, defaults to .today()
    :return: True if the person was born in the last 30 days, false otherwise.
    """
    return is_n_days_after(person, "BIRT", 30, from_date)
