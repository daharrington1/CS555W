# from Utils.Utils import getParent2ChildrenMap


def us14_mult_births(ind_map=None, fam_map=None, count=2):
    """
    Returns siblings with birthdays greating than a given count
    User Story 14: count is 14

    :param Families and Individual lists
    :returns List of Siblings greater than the count
    """

    if (ind_map is None) or (fam_map is None):
        raise Exception(ValueError, "Missing Inputs")

    ret = []  # list of suspect fam_map

    for id, fam in fam_map.items():
        birthdays = {}
        for child in fam["CHIL"]:
            birthdays.setdefault(str(ind_map[child]["BIRT"][1])+'/'+str(ind_map[child]["BIRT"][0])+'/'+str(ind_map[child]["BIRT"][2]), []).append(child)

        for bday, ids in birthdays.items():
            if len(ids) >= count:
                ret.append((sorted(ids), bday))

    # return all matches
    return ret
