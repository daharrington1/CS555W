from Utils import Logger


def is_leap_year(year):
    """
    Checks if the current year is a leap year on the Gregorian Calendar
    :param year: The integer year to check
    :return: True if a leap year, false otherwise
    """
    # If year is divisible by four and not on a century, unless that century is divisible by 400 is the formula
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


class DateValidator:
    _logger = None
    month_map = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    def __init__(self, logger):
        self._logger = logger

    def _log(self, date, is_individual):
        self._logger.log_error(42, is_individual, "{} is an invalid date".format(date))

    def validate_date(self, date, is_individual=True):
        """
        Checks if a date is a valid format
        :param date: The date list to check in integer from of [day, month, year]
        :param is_individual: To determine the log label, assumed true if not specified
        :return: True if a valid date, false otherwise
        """
        if len(date) != 3 or type(date) is not list:
            self._log(date, is_individual)
            return False

        day = date[0]
        if day < 1 or day > 31:
            self._log(date, is_individual)
            return False

        month = date[1]
        # February handling because it has to be difficult
        # Only need to check for a valid leap day, as the below return handles the normal 28 days
        if month == 2 and day == 29 and is_leap_year(date[2]):
            return True

        try:
            return day <= self.month_map[month]
        except KeyError:
            return False
