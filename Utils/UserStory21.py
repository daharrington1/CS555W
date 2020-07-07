def find_mistitled_spouse(individuals, families):
    """
    Ensure that all individuals in a family match have the correct title
    Ie, women are under wife and men are listed under husband
    :param individuals: All individuals, keyed by INDI id, and has INDI in the dictionary body
    :param families: All families, which must have HUSB and WIFE tags
    :return: A list of all ids which are mistitled
    """
    mismatched_ids = []
    for family in families:
        mismatched_ids += filter_differing_sex(_from_id(family["HUSB"], individuals), "M")
        mismatched_ids += filter_differing_sex(_from_id(family["WIFE"], individuals), "F")

    return mismatched_ids


def filter_differing_sex(individuals, target_sex):
    """
    Filters out all individuals which sex does not match the provided target
    :param individuals: A list of individuals to check which contain INDI and SEX field
    :param target_sex: The sex to filter against, should be M or F.
    :return: A list of all ids which do not exactly match the specified target
    """
    return [individual["INDI"] for individual in individuals if individual["SEX"] != target_sex]


def _from_id(targets, full_list):
    return [full_list[target] for target in targets if target != "-"]
