from Utils.Utils import normalize_family_entry, getSpouses


def us16_male_last_names(indMap, famMap):
    """
    User Story 16: Checks for Male Last Names

    :param Individuals and Family lists
    :returns List of Familes where the males don't all have the same last name in their family
    """
    male_lastnames = []  # list of suspect families

    if (indMap is None) or (famMap is None):
        raise Exception(ValueError, "Missing Inputs")

    for id, fam in famMap.items():
        lastNames = set()

        # assume it is a bad family at first
        badFam = {"FAM": id}

        # look at all spouses in case information is backwards
        spouses = getSpouses(fam)
        for male in spouses:
            # skip over anyone not identified as a male
            if indMap[male]["SEX"] == 'M':
                lastNames.add(indMap[male]["NAME"].split("/")[1])

        # look at male children last names
        for child in fam["CHIL"]:
            # only look at males and non-unique last names
            if indMap[child]["SEX"] == 'M':
                lastNames.add(indMap[child]["NAME"].split("/")[1])

        # check for unique male last names in families
        if len(lastNames) > 1:
            badFam["LNAMES"] = lastNames
            male_lastnames.append(badFam)

    return male_lastnames
