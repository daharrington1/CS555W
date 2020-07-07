# The UserStory program by developer&tester Chengyi Zhang
from Utils.Utils import normalize_family_entry, getSpouses
import datetime


def us39_upcoming_anniversaries(individuals, families):
    """
    User Story 39: List all living couples in a GEDCOM file whose marriage
                   anniversaries occur in the next 30 days

    :param Individuals and Family lists
    :returns List of all living couples with upcoming anniversaries
    """
    ret = []
    deadList = {}  # map of dead individuals

    # build map of id to mail last names
    for ind in individuals:
        if "DEAT" in ind and type(ind["DEAT"]) is list:
            # print("Adding Id({}), Name({}), sex({}) to in2Name: ".format(ind["INDI"], ind["NAME"], ind["SEX"]))
            deadList[ind["INDI"]] = ind

    for fam in families:
        fam = normalize_family_entry(fam)

        # skip over divorced people
        if fam["DIV"] is not None:
            continue

        # check if any of the spouses are dead - if so - skip them
        widower = False
        spouses = getSpouses(fam)
        for spouse in spouses:
            if spouse in deadList:
                widower = True
                break

        if widower:
            continue

        # see if the anniversary is within 30 days
        date_diff = datetime.datetime(datetime.datetime.today().year, fam['MARR'][1], fam['MARR'][0]) - datetime.datetime.today()
        if (date_diff > datetime.timedelta(days=0) and date_diff < datetime.timedelta(days=30)):
            ret.append((fam['FAM'], fam['MARR']))

    return ret
