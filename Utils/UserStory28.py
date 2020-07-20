
def sort_children_by_age(family, all_individuals):
    """
    Returns all children sorted in descending order by age
    :param family: The family to check for, if the CHIL tag is not present, returns the []
    :param all_individuals: All individuals, keyed by the INDI. Should have INDI, AGE, and NAME fields
    :return: The sorted list, or the empty list for no children
    """
    try:
        children_ids = family["CHIL"]
    except KeyError:
        return []
    children = [all_individuals[child_id] for child_id in children_ids if child_id in all_individuals]
    children.sort(key=lambda child: child["AGE"], reverse=True)
    return children

