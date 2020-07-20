
def us15_sibling_count(fam_map=None, count=1):
    """
    Returns siblings greating than a given count
    User Story 15: count is 15

    :param Families and Individual lists
    :returns List of Siblings greater than the count
    """

    if (fam_map is None):
        raise Exception(ValueError, "Missing Inputs")

    ret = []  # list of suspect fam_map

    for id, fam in fam_map.items():
        # can't have more than 15 siblings in a family - includes half-siblings
        if len(fam["CHIL"]) >= count:
            ret.append((id, sorted(fam["CHIL"])))

    # return all matches
    return ret
