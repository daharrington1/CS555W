from Utils.Utils import normalize_family_entry, getSpouses


def us16_male_last_names(indMap, fam, logger):
    """
    User Story 16: Checks for Male Last Names

    :param Individuals and Family lists
    :returns List of Familes where the males don't all have the same last name in their family
    """
    if (indMap is None) or (fam is None) or (logger is None):
        raise Exception(ValueError, "Missing Inputs")

    lastNames = set()   # define as set to be unique names

    # look at all mail spouses
    for male in getSpouses(fam):
        if indMap[male]["SEX"] == 'M':
            lastNames.add(indMap[male]["NAME"].split("/")[1])

    # look at male children last names
    for child in fam["CHIL"]:
        if indMap[child]["SEX"] == 'M':
            lastNames.add(indMap[child]["NAME"].split("/")[1])

    # check for unique male last names in families
    if len(lastNames) > 1:
        logger.log_family_warning(16, "{} has multiple last names: {}".format(
                               fam["FAM"], sorted(lastNames)))
