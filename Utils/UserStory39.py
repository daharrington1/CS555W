from Utils.Utils import getSpouses, check_dates
import datetime


def us39_upcoming_anniversaries(ind_map, fam, logger):
    """
    User Story 39: List all living couples in a GEDCOM file whose marriage
                   anniversaries occur in the next 30 days

    :param Individuals and Family lists
    :returns List of all living couples with upcoming anniversaries
    """
    # build map of id to mail last names
    # check non-divorced couples and non-widowers
    # print("\nfam: {}".format(fam))
    if len(fam["DIV"]) > 0:
        print("Family {} is divorced".format(fam["FAM"]))
        return

    Widower = False
    for spouse in getSpouses(fam):
        if "DEAT" in ind_map[spouse] and type(ind_map[spouse]["DEAT"]) is list:
            Widower = True

    # check if the anniversary is within 30 days
    if not Widower:
        try:
            if check_dates(datetime.date(datetime.date.today().year, fam['MARR'][1],
                           fam['MARR'][0]), datetime.date.today(), 30, 'days', upcoming=True):
                # print("Family {} has upcoming anniversary: {}".format(fam["FAM"], fam["MARR"]))
                logger.log_family_info(39, "FAMILY ({}) has an upcoming anniversary: {}".format(
                                       fam["FAM"], str(fam['MARR'][1])+'/'+str(fam['MARR'][0])+'/'+str(fam['MARR'][2])))
        except Exception:
            return # problem with dates - skip this entry
    return



