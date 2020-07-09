from Utils.Utils import getMaritalStatus


def us31_get_single_individuals(ind_map=None, fam_map=None):
    """
    User Story 31: Get Single Individuals

    :param Familie and Individual lists
    :returns List of Single Individuals
    """

    if (ind_map is None) or (fam_map is None):
        raise Exception(ValueError, "Missing Inputs")

    # declare empty list
    ret = []  # list of mappings of parent to siblings

    results = getMaritalStatus(ind_map, fam_map)  # create a map of all parents to children

    for ind in results:
        if results[ind]["Status"] == "Single":
            ret.append(ind)

        # if results[ind]["Status"]=="Dead":
        # print("Dead Person: {}".format(ind))

        # if results[ind]["Status"]=="Divorced":
        # print("Divorced Person: {}".format(ind))

        # if results[ind]["Status"]=="Widower":
        # print("Widowed Person: {}".format(ind))

    # return all matches
    return ret
