from Utils.Utils import getParent2ChildrenMap, normalize_spouse_ids


def us18_no_siblingmarriages(individuals=None, families=None):
    """
    User Story 18: Checks for Families where spouses are siblings
                   Siblings include half siblings also

    :param Familie and Individual lists
    :returns List of Familees that have sblings as spouses
    """

    if (individuals is None) or (families is None):
        raise Exception(ValueError, "Missing Inputs")

    # declare empty list
    ret = []  # list of mappings of parent to siblings

    parentId2Children = getParent2ChildrenMap(families)  # create a map of all parents to children

    for fam in families:
        # get all husband/wives in the family and check to see if their spouse is their child
        #spouses = getSpousesInFamily(fam)
        spouses = normalize_spouse_ids(fam)
        # print("spouses: {}".format(spouses))

        # loop thru parentId2Children and see if there is an intersection of spouses and children
        for item in parentId2Children:
            # print("children: {}".format(parentId2Children[item]))
            if len(set(parentId2Children[item]).intersection(set(spouses))) > 1:
                # print("intersection: fam: {}".format(fam))
                tmp = {"Parents": set(parentId2Children[item]).intersection(set(spouses)), "FAM": fam["FAM"]}
                ret.append(tmp)
                break

    # return all matches
    return ret
