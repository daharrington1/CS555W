def us16_male_last_names(individuals, families):
    """
    User Story 16: Checks for Male Last Names

    :param Individuals and Family lists
    :returns List of Familes where the males don't all have the same last name in their family
    """
    male_lastnames = []  # list of suspect families
    id2Name = {}  # mapping of male ids to last name

    if (individuals is None) or (families is None):
        raise Exception(ValueError, "Missing Inputs")

    # build map of id to mail last names
    for ind in individuals:
        if ind["SEX"] == "M":  # only store male names
            id2Name[ind["INDI"]] = ind["NAME"].split("/")[1]

    for fam in families:
        lastNames = []

        # assume it is a bad family at first
        badFam = {"FAM": fam["FAM"]}

        # look at husbands last names
        if ("HUSB" in fam) and type(fam["HUSB"]) is list:

            for male in fam["HUSB"]:
                if male not in id2Name:
                    raise Exception(ValueError, "Husband {} is not in the male mapping".format(male))

                if id2Name[male] not in lastNames:
                    lastNames.append(id2Name[male])

        # look at male children last names
        if ("CHIL" in fam) and type(fam["CHIL"]) is list:
            for child in fam["CHIL"]:
                # only look at males and non-unique last names
                if child in id2Name and id2Name[child] not in lastNames:
                    lastNames.append(id2Name[child])

        # check for unique male last names in families
        if len(lastNames) > 1:
            badFam["LNAMES"] = lastNames
            male_lastnames.append(badFam)

    return male_lastnames
