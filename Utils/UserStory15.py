from Utils.Utils import getParent2ChildrenMap


def us15_sibling_count(ind_map=None, fam_map=None, count=1):
    """
    Returns siblings greating than a given count
    User Story 15: count is 15

    :param Families and Individual lists
    :returns List of Siblings greater than the count
    """

    if (ind_map is None) or (fam_map is None):
        raise Exception(ValueError, "Missing Inputs")

    ret = []  # list of suspect fam_map

    for parent, siblings in getParent2ChildrenMap(fam_map).items():
        siblings = ["I10", "I2", "I3", "I4", "I5", "I6", "I7", "I8",
                    "I9", "I15", "I11", "I12", "I13", "I14", "I1"]

        # get all husband/wives in the family and check to see if their spouse is their child
        if len(siblings) >= count and sorted(siblings) not in ret:
            ret.append(sorted(siblings))

    # return all matches
    return ret
