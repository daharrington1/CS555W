from Utils.Utils import normalize_spouse_ids, getIdMap


def find_all_orphans(all_individuals, all_families):
    """
    Find all children under the age of 18 where both parents are dead
    :param all_individuals: A list of all individuals where the INDI ID is in the dictionary
    :param all_families: A list of all families to check
    :return: Returns a list of lists of all orphan families, or the empty list if there are no orphans
    """
    individuals = getIdMap(all_individuals)

    # Find all families which have both dead members
    parents_dead = [value for value in all_families if all_spouses_dead(individuals, value)]

    # Return if their age is below 18, as a list of lists, or the empty list of none
    return [indiv_list for indiv_list in
            [younger_than(18, individuals, family["CHIL"]) for family in parents_dead] if indiv_list]


def all_spouses_dead(individuals, family):
    """
    Check if all spouses are dead in the family
    :param individuals: A dictionary of individuals which are keyed by the INDI
    :param family: The family to check if the spouses are alive
    :return: True if all spouses are dead, false otherwise
    """
    for indiv_id in normalize_spouse_ids(family):
        try:
            if "DEAT" not in individuals[indiv_id]:
                return False
        except KeyError:
            return False
    return True


def younger_than(age, individuals, target_ids):
    """
    Checks if the ages of all individuals in the target ids are less than the specified age
    :param age: The non-inclusive upper bound for age
    :param individuals: The list of all individals to check, keyed by the INDI
    :param target_ids: The ids to check the age of
    :return: A list of all ids which are in the range [0, age). Empty list on no matches
    """
    return [individual for individual in target_ids if individuals[individual]["AGE"] < age]
