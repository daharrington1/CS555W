import datetime
from Utils.Utils import check_dates
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
            if not check_dates(current.time, older_sibling.time, 1, "days") and \
                    check_dates(current.time, older_sibling.time, 8, "months"):
                ids.add(current.id)
                ids.add(older_sibling.id)

    return ids


def _from_id(targets, full_list):
    # Duplicate of US21, update in refactor
    return [full_list[target] for target in targets if target != "-"]


def _as_dateTime(date, individual_id):
    return DateTimeForID(datetime.datetime(date[2], date[1], date[0]), individual_id)
