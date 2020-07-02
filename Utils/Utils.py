from collections import namedtuple
import datetime

BirthDateKeyedIndividual = namedtuple('BirthdayKeyedIndividual', 'birthday name id')


def filter_non_unique_individuals(individuals):
    """
     Filters a list of individuals to find any individuals which do not have a unique combination of BirthDate + name

     Return dictionary is keyed by <birthday><name>, and the value is a list of all conflicts
        Ie someone born on January 3rd, 2000 with the name John Smith would be keyed as
        [3, 1, 2000]John /Smith/
        assuming both fields were inputted as they are stored in the database layer. This function is capable of
        reducing on any format of the two, as long as all individuals maintain the same form.

        The conflicts will be a list of BirthDateKeyedIndividuals

     Note: A birth date includes the year; as such a John Smith born on January 1st, 2000 and a John Smith born on
        January 1st, 2001 are unique. They share a birthday, but not a birth date.

    :raises KeyError if an individual dictionary is missing one of the required keys.
        Code raises instead of dropping malformed values as there is no valid use case for a missing tag
    :param individuals A list of dictionaries which include the INDI, NAME, and BIRT tags
    :returns A dictionary of all conflicts where the values are the list of BirthDateKeyedIndividuals
    """
    birthday_name_mapping = {}
    # Convert the required fields into a tuple for immutability and readability once returned
    for individual in [BirthDateKeyedIndividual(indiv['BIRT'], indiv["NAME"], indiv["INDI"]) for indiv in individuals]:
        # Create the derived key to allow for constant look up, and chain on collisions
        key = "{}{}".format(individual.birthday, individual.name)
        birthday_name_mapping[key] = birthday_name_mapping.get(key, []) + [individual]

    # Return only the collisions as they are therefore not unique
    return {key: value for key, value in birthday_name_mapping.items() if len(value) > 1}


def getIdMap(key, records):
    """
     Build a map of id to their record
    :param List of either Individuals and Families from the database
    :returns Map of all IDs to record
    """
    idMap = {}
    for record in records:
        idMap.setdefault(record[key], record)

    return idMap


def getDateTimestamp(date):
    """
     Convert the array date value to a date timestamp
    :param Single Date in an array
    :returns Timestamp of the date
    """
    if date == [] or date == '':
        return -1

    # convert to timestamp - inputs: year/month/date
    date_timestamp = datetime.datetime(date[2], date[1], date[0]).timestamp()
    return date_timestamp


def getParent2ChildrenMap(families):
    """
     Build a map of parent to children - crosses families
     if married more than once
    :param List of Individuals and Families
    :returns Map of all Parent IDs to Children
    """
    parentId2Children = {}

    for fam in families:

        # don't need to do anything if there's no children
        if ("CHIL" in fam) and type(fam["CHIL"]) is list:

            # add child to parent id mapping
            for child in fam["CHIL"]:
                # build husband parent to child mapping
                if ("HUSB" in fam) and type(fam["HUSB"]) is list:
                    for husb in fam["HUSB"]:
                        if husb in parentId2Children:
                            if child not in parentId2Children[husb]:
                                parentId2Children[husb].append(child)
                        else:
                            parentId2Children[husb] = []
                            parentId2Children[husb].append(child)

                # build husband parent to child mapping
                if ("WIFE" in fam) and type(fam["WIFE"]) is list:
                    for wife in fam["WIFE"]:
                        if wife in parentId2Children:
                            if child not in parentId2Children[wife]:
                                parentId2Children[wife].append(child)
                        else:
                            parentId2Children[wife] = [child]

    return parentId2Children


def getSpouses(fam):
    """
     Return all spouses in the family, excluding '-'
     All values returned in an array, including empty array
    :param a single family
    :returns my spouse(s) in the given family
    """
    spouses = []
    for key in ["HUSB", "WIFE"]:
        if key in fam and type(fam[key]) is list and key not in spouses:
            spouses += fam[key]

    # print ("[getSpouses] FAM({}), spouses: {}".format(fam["FAM"], spouses))
    return spouses


def getMySpouses(id, fam):
    """
     Figure out My Spouse in the current family
     Calls getSpouses which skips '-' entries
    :param a single family
    :returns my spouse(s) in the given family
    """
    # get all the spouses in the family
    spouses = getSpouses(fam)
    mySpouses = []

    # remove myself from the list of all spouses
    for sid in spouses:
        if sid != id and sid != '-' and sid not in mySpouses:
            mySpouses.append(sid)

    # print("[getMySpouses] Me({}), my spouses: {}".format(id, mySpouses))
    return mySpouses


def getLatestDate(i_dates):
    """
     Return the latest date in an array of dates
    :param List of dates
    :returns the latest date
    """
    # for date in dates:
    # print("Latest Dates: date: {}".format(date))
    dates = i_dates.copy()

    if len(dates) < 1:
        return []

    # pop the first date off the list for a comparison
    latest_date = dates.pop()

    # loop through the rest of the dates for a larger date
    for date in dates:
        if getDateTimestamp(date) > getDateTimestamp(latest_date):
            latest_date = date

    return latest_date


def single_parent(fam):
    """
     Determine if the family is a single parent family
    :param Family object
    :returns true if the family is a single parent family.
    """
    ret = False

    # make every thing and array or None
    fam = normalize_family_entry(fam)

    # check for single parent
    if fam["WIFE"] is not None and len(fam["WIFE"]) == 1 and fam["HUSB"] is None:
        ret = True

    # check for single parent
    if fam["HUSB"] is not None and len(fam["HUSB"]) == 1 and fam["WIFE"] is None:
        ret = True

    return ret


def get_marriage_status(entry):
    """
     Determine the marriage status of a person
    :param List of Marriage/Divorce/Widow status for the given person
    :returns the marital status
    """
    # look at all the divorced, widowed and married peoplee
    if getDateTimestamp(getLatestDate(entry["WIDOWER"])) > getDateTimestamp(getLatestDate(entry["DIV"])) and  \
       getDateTimestamp(getLatestDate(entry["WIDOWER"])) > getDateTimestamp(getLatestDate(entry["MARR"])):
        return "Widower"

    if getDateTimestamp(getLatestDate(entry["DIV"])) > getDateTimestamp(getLatestDate(entry["WIDOWER"])) and  \
       getDateTimestamp(getLatestDate(entry["DIV"])) > getDateTimestamp(getLatestDate(entry["MARR"])):
        return "Divorced"

    return "Married"


def update_marriage_info(fam, spouse, individuals, Id2MarrStatus):
    """
     Update Id2MarrStatus with the marital information
     of the given id in the family
    :param spouse, family object and Id2MarrStatus Map
    :returns Updated Id2MarrStatus Map
    """
    indMap = getIdMap('INDI', individuals)
    fam = normalize_family_entry(fam)
    # If there is a divorce date - then you can't still
    # be married or a widower to this person
    if fam["DIV"] is not None:
        Id2MarrStatus[spouse]["DIV"].append(fam["DIV"])
    elif fam["MARR"] is not None:
        # you are married or a widower
        for my_spouse in getMySpouses(spouse, fam):
            # you are either married to spouse or windower
            # print("FAM ({}), ee({}), my spouse: {}".format(fam["FAM"], person, my_spouse))
            if "DEAT" in indMap[my_spouse] and \
               type(indMap[my_spouse]["DEAT"]) is list:
                Id2MarrStatus[spouse]["WIDOWER"].append(indMap[my_spouse]["DEAT"])
            else:
                # if you are not a widower, then you are still
                # married to this person
                Id2MarrStatus[spouse]["MARR"].append(fam["MARR"])

    return Id2MarrStatus


def getMaritalStatus(individuals, families):
    """
     Build a map of person to marriage/divorces
    :param List of Families
    :returns Map of all IDs to Marriage/Divorces
    """
    # build a map of marriages and divorces for each spouse in a family
    Id2MarrStatus = {}
    for fam in families:
        # check for single parent
        if single_parent(fam):
            continue

        # print("\n\nLOOKING AT FAMILY: {}".format(fam))
        for spouse in getSpouses(fam):
            if spouse not in Id2MarrStatus:
                Id2MarrStatus[spouse] = {"MARR": [], "DIV": [], "WIDOWER": [], "Status": ''}
            update_marriage_info(fam, spouse, individuals, Id2MarrStatus)

    for ind in individuals:
        key = ind["INDI"]

        # Initialize the entry as being single
        if key not in Id2MarrStatus:
            Id2MarrStatus[key] = {"MARR": [], "DIV": [], "WIDOWER": [], "DEAT": [], "Status": 'Single'}

        # check if this person is dead - if so, then are not married, divorce or single
        if "DEAT" in ind and type(ind["DEAT"]) is list:
            Id2MarrStatus[key]["DEAT"] = ind["DEAT"]
            Id2MarrStatus[key]["Status"] = "Dead"
        elif key in Id2MarrStatus and Id2MarrStatus[key]["Status"] != 'Single':
            # check if they are married
            Id2MarrStatus[key]["Status"] = get_marriage_status(Id2MarrStatus[key])

    return Id2MarrStatus


def normalize_family_entry(i_fam):
    """
    Normalizes all arrays in family entry
    :param family: The family object
    :return: all the keys that take arrays are arrays
    """
    fam = i_fam.copy()
    keys = ["MARR", "DIV", "HUSB", "WIFE"]
    for key in keys:
        if key not in fam or fam[key] == '-':
            fam[key] = None

    return fam


def normalize_spouse_ids(family):
    """
    Normalizes the spouse ids of a family into a flat list
    :param family: The family object to get the spouse ids from
    :return: A flat list of ids, or the empty list if no ids exist
    """
    ids = []
    for key in ["HUSB", "WIFE"]:
        if key not in family:
            continue
        ids += family[key] if type(family[key]) is list else [family[key]]
    return ids
