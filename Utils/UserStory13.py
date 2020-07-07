import datetime
from Utils.DateValidator import day_mapping_for_year
from collections import namedtuple

DateTimeForID = namedtuple('DateTimeForID', 'time id')


def find_invalid_sibling_spacing(individuals, families):
    """
    Checks if all siblings in a family are not twins (more than 1 day apart), and less than 8 months apart
    :param individuals: Individuals dictionary keyed by ID and has INDI and BIRT fields
    :param families: All families to check. If CHIL is present, is must be a list
    :return: A set of all ids born in the range (2 days, 8 months) of each other
    """
    ids = set()

    for family in [family for family in families if "CHIL" in family]:
        # Get all the children in the family, and sort based on birth date with the oldest first
        children = _from_id(family["CHIL"], individuals)
        datetimes = [_as_dateTime(child["BIRT"], child["INDI"]) for child in children]
        datetimes.sort(key=lambda it: it[0])

        # Check if every child is spaced correctly compared to the previous, if the validation fails add both to the
        # resulting set
        for index in range(1, len(datetimes)):
            current, older_sibling = datetimes[index], datetimes[index-1]
            if _births_in_range(1, 8, current.time, older_sibling.time):
                ids.add(current.id)
                ids.add(older_sibling.id)

    return ids


def n_months_ago(from_datetime, distance):
    """
    Converts a date object to one that is N months in the past
    This function is useful compared to timestamps if the date is pre 1970 as the datetime library can overflow
    :param from_datetime: The datetime to start from
    :param distance: The amount of months to reverse, must be non-negative
    :raise ValueError when distance is negative
    :return: The datetime N months in the passed, with the day moved to the last valid day of the month
    """
    if distance < 0:
        raise ValueError("Distance must be non-negative")
    year_change = distance // 12
    distance %= 12

    in_year_distance = from_datetime.month - distance
    if in_year_distance == 0:
        new_month = 1
    elif in_year_distance < 0:
        year_change += 1
        # Subtract from 13 as months are 1 indexed and not zero
        new_month = 13 - (distance - from_datetime.month)
    else:
        new_month = from_datetime.month - distance

    new_year = from_datetime.year - year_change
    day_mapping = day_mapping_for_year(new_year)

    return datetime.datetime(new_year,
                             new_month,
                             from_datetime.day if from_datetime.day <= day_mapping[new_month]
                             else day_mapping[new_month])


def _births_in_range(min_days, max_months, reference_birth, older_sibling_birth):
    this_birth = reference_birth
    older_sibling_birth = older_sibling_birth
    twin_cutoff = this_birth - datetime.timedelta(days=min_days)
    normal_cutoff = n_months_ago(this_birth, max_months)
    return normal_cutoff < older_sibling_birth < twin_cutoff


def _from_id(targets, full_list):
    # Duplicate of US21, update in refactor
    return [full_list[target] for target in targets if target != "-"]


def _as_dateTime(date, individual_id):
    return DateTimeForID(datetime.datetime(date[2], date[1], date[0]), individual_id)
