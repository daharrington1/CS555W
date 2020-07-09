from Utils.Utils import getSpouses, check_dates
import datetime


def us39_upcoming_anniversaries(ind_map, fam_map):
    """
    User Story 39: List all living couples in a GEDCOM file whose marriage
                   anniversaries occur in the next 30 days

    :param Individuals and Family lists
    :returns List of all living couples with upcoming anniversaries
    """
    ret = []

    # build map of id to mail last names
    for fam_id, fam in fam_map.items():
        # check non-divorced couples and non-widowers
        if len(fam["DIV"]) < 1:
            Widower=False
            for spouse in getSpouses(fam):
                if "DEAT" in ind_map[spouse] and type(ind_map[spouse]["DEAT"]) is list:
                    Widower=True

            # check if the anniversary is within 30 days
            if not Widower:
                try:
                    if check_dates(datetime.date(datetime.date.today().year, fam['MARR'][1],
                                   fam['MARR'][0]), datetime.date.today(), 30, 'days', upcoming=True):
                        ret.append((fam_id, fam['MARR']))
                except Exception:
                    continue    # problem with dates - skip this entry
    return ret
