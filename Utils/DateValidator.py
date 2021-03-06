def is_leap_year(year):
    """
    Checks if the current year is a leap year on the Gregorian Calendar
    :param year: The integer year to check
    :return: True if a leap year, false otherwise
    """
    # If year is divisible by four and not on a century, unless that century is divisible by 400 is the formula
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def day_mapping_for_year(year):
    """
    Gets a copy of the month to day mapping for a given year. Handles leap year check for February.
    :param year: The year to check for in the day_mapping
    :return: A copy of month_map with February updated to the correct leap year value
    """
    day_mapping = month_map.copy()
    if is_leap_year(year):
        day_mapping[2] = 29
    return day_mapping


month_map = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


class DateValidator:
    _logger = None

    def __init__(self, logger):
        self._logger = logger

    def _log(self, date, is_individual):
        self._logger.log_error(42, is_individual, "{} is an invalid date".format(
            format_date(date, date)))

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
        try:
            return day <= day_mapping_for_year(date[2])[month]
        except KeyError:
            return False


def format_date(date, error_value):
    """
    Converts a list date to a date for output
    :param date as a list, with indexes [day, month, year]
    :param error_value is the value to use in error cases
    :return: String of the format in DD/MM/YYYY if valid format, otherwise strips [] from list toString
    """
    if type(date) is not list or len(date) < 3:
        # Mal formed date, do not attempt to parse
        return error_value
    # DD MM YYYY.
    return "{:02d}/{:02d}/{:04d}".format(date[0], date[1], date[2])
