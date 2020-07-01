from Utils.Utils import getParent2ChildrenMap, normalize_spouse_ids, getMySpouse


def us17_no_marr2child(individuals=None, families=None):
    """
    User Story 17: Checks for Families where a spouse is married to a child

    :param Families and Individual lists
    :returns List of Familes that have a spouse married to a child
    """

    if (individuals is None) or (families is None):
        raise Exception(ValueError, "Missing Inputs")

    ret = []  # list of suspect families
    parentId2Children = getParent2ChildrenMap(families)  # create a map of all parents to children

    for fam in families:
        # get all husband/wives in the family and check to see if their spouse is their child
        spouses = normalize_spouse_ids(fam)
        for spouse in spouses:
            mySpouses = getMySpouse(spouse, fam)  # just in case you have more than one spouse
            for myspouse in mySpouses:
                # get all my children and check if spouse is in them
                if spouse in parentId2Children:
                    children = parentId2Children[spouse]
                    if myspouse in children:
                        # my spouse is married to my child
                        tmp = {"Spouse": spouse, "MySpouse": myspouse, "FAM": fam["FAM"], "MyChildren": children}
                        ret.append(tmp)
    # return all matches
    return ret
