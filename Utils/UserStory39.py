# The UserStory program by developer&tester Chengyi Zhang
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
    deadList = {}  # map of dead individuals

    # build map of id to mail last names
    for fam_id, fam in fam_map.items():
        # check non-divorced couples and non-widowers 
        if len(fam["DIV"]) < 1:
            for spouse in getSpouses(fam):
                if "DEAT" in ind_map[spouse] and type(ind_map[spouse]["DEAT"]) is list:
                    continue

            # check if the anniversary is within 30 days
            try:
                if check_dates(datetime.date(datetime.date.today().year, fam['MARR'][1], 
                               fam['MARR'][0]), datetime.date.today(), 30, 'days', upcoming=True):
                    ret.append((fam_id, fam['MARR']))
            except Exception:
                continue    # problem with dates - skip this entry
    return ret
