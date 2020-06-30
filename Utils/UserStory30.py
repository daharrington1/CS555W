from collections import namedtuple
from pprint import pprint
from Utils.Utils import getMaritalStatus


def us30_get_married_individuals(individuals=None, families=None):
    """
    User Story 30: Get Married Individuals

    :param Familie and Individual lists
    :returns List of Married Individuals
    """

    if (individuals == None) or (families == None):
        raise Exception(ValueError, "Missing Inputs")

    # declare empty list
    ret = []  # list of mappings of parent to siblings

    results = getMaritalStatus(individuals, families)  # create a map of all parents to children

    for ind in results:
        if results[ind]["Status"] == "Married":
            ret.append(ind)

    # return all matches
    return ret;
