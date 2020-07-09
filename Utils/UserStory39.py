# The UserStory program by developer&tester Chengyi Zhang
from Utils.Utils import normalize_family_entry, getSpouses, check_dates
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
    for ind_id, ind in ind_map.items():
        if "DEAT" in ind:
            # print("Adding Id({}), Name({}), sex({}) to in2Name: ".format(ind["INDI"], ind["NAME"], ind["SEX"]))
            deadList[ind_id] = ind

    for fam_id, fam in fam_map.items():
        # skip over divorced people
        if len(fam["DIV"]) > 0:
            continue

        # check if any of the spouses are dead - if so - skip them
        widower = False
        for spouse in getSpouses(fam):
            if spouse in deadList:
                widower = True
                break

        if not widower:
            # see if the anniversary is within 30 days
            try:
                if check_dates(datetime.date(datetime.date.today().year, fam['MARR'][1], fam['MARR'][0]), datetime.date.today(), 30, 'days', upcoming=True):
                    ret.append((fam_id, fam['MARR']))
            except Exception:
                continue    # problem with dates - skip this entry

    return ret
