from Utils.Utils import getMaritalStatus


def us30_get_married_individuals(ind_map=None, fam_map=None):
    """
    User Story 30: Get Married Individuals

    :param Familie and Individual lists
    :returns List of Married Individuals
    """

    if (ind_map is None) or (fam_map is None):
        raise Exception(ValueError, "Missing Inputs")

    # declare empty list
    ret = []  # list of mappings of parent to siblings

    results = getMaritalStatus(ind_map, fam_map)  # get Marital Status

    for ind in results:
        if results[ind]["Status"] == "Married":
            ret.append(ind)

    # return all matches
    # print("Results: {}".format(ret))
    return ret
