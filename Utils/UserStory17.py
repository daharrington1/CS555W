from Utils.Utils import getParent2ChildrenMap, getSpouses, getMySpouses


def us17_no_marr2child(ind_map=None, fam_map=None):
    """
    User Story 17: Checks for Families where a spouse is married to a child

    :param Families and Individual lists
    :returns List of Familes that have a spouse married to a child
    """

    if (ind_map is None) or (fam_map is None):
        raise Exception(ValueError, "Missing Inputs")

    ret = []  # list of suspect fam_map
    parentId2Children = getParent2ChildrenMap(fam_map)  # create a map of all parents to children

    for fam_id, fam in fam_map.items():
        # get all husband/wives in the family and check to see if their spouse is their child
        for spouse in getSpouses(fam):
            for myspouse in getMySpouses(spouse, fam):
                # get all my children and check if spouse is in them
                if spouse in parentId2Children:
                    children = parentId2Children[spouse]
                    if myspouse in children:
                        # my spouse is married to my child
                        tmp = {"Spouse": spouse, "MySpouse": myspouse, "FAM": fam_id, "MyChildren": children}
                        ret.append(tmp)
    # return all matches
    return ret
