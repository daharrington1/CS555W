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
    try:
        date_timestamp = datetime.datetime(date[2], date[1], date[0]).timestamp()
        return date_timestamp
    except Exception:
        return -1


def getParent2ChildrenMap(fam_map):
    """
     Build a map of parent to children - crosses families
     if married more than once
    :param List of Individuals and Families
    :returns Map of all Parent IDs to Children
    """
    parentId2Children = {}

    # build parent to child mapping
    for fam_id, fam in fam_map.items():
        for child in fam["CHIL"]:
            for spouse in getSpouses(fam):
                if spouse in parentId2Children and child not in parentId2Children[spouse]:
                    parentId2Children[spouse].append(child)
                else:
                    parentId2Children[spouse] = [child]

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
        for spouse in fam[key]:
            spouses.append(spouse) if spouse not in spouses else spouses

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
    for spouse in spouses:
        mySpouses.append(spouse) if spouse != id and spouse not in mySpouses else mySpouses

    # print("[getMySpouses] Me({}), my spouses: {}".format(id, mySpouses))
    return mySpouses


def getLatestDate(dates):
    """
     Return the latest date in an array of dates
    :param List of dates
    :returns the latest date
    """
    # for date in dates:
    # print("Latest Dates: date: {}".format(date))
    if len(dates) < 1:
        return []

    # just set the first date to the latest date
    latest_date = dates[0]

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
    return ((len(fam["WIFE"]) == 1 and len(fam["HUSB"]) < 1) or (len(fam["HUSB"]) == 1 and len(fam["WIFE"]) < 1))


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


def update_marriage_info(fam, spouse, ind_map, Id2MarrStatus):
    """
     Update Id2MarrStatus with the marital information
     of the given id in the family
    :param spouse, family object and Id2MarrStatus Map
    :returns Updated Id2MarrStatus Map
    """
    # If there is a divorce date - then you can't still
    # be married or a widower to this person
    if len(fam["DIV"]) > 0:
        Id2MarrStatus[spouse]["DIV"].append(fam["DIV"])
    elif len(fam["MARR"]) > 0:
        # you are married or a widower
        for my_spouse in getMySpouses(spouse, fam):
            # you are either married to spouse or windower
            # print("FAM ({}), ee({}), my spouse: {}".format(fam["FAM"], person, my_spouse))
            if "DEAT" in ind_map[my_spouse] and \
               type(ind_map[my_spouse]["DEAT"]) is list:
                Id2MarrStatus[spouse]["WIDOWER"].append(ind_map[my_spouse]["DEAT"])
            else:
                # if you are not a widower, then you are still
                # married to this person
                Id2MarrStatus[spouse]["MARR"].append(fam["MARR"])

    return Id2MarrStatus


def getMaritalStatus(ind_map, fam_map):
    """
     Build a map of person to marriage/divorces
    :param List of Families
    :returns Map of all IDs to Marriage/Divorces
    """
    # build a map of marriages and divorces for each spouse in a family
    Id2MarrStatus = {}
    for fam_id, fam in fam_map.items():
        # check for single parent
        if not single_parent(fam):
            # print("\n\nLOOKING AT FAMILY: {}".format(fam))
            for spouse in getSpouses(fam):
                if spouse not in Id2MarrStatus:
                    Id2MarrStatus[spouse] = {"MARR": [], "DIV": [], "WIDOWER": [], "Status": ''}
                update_marriage_info(fam, spouse, ind_map, Id2MarrStatus)

    for key, ind in ind_map.items():

        # Initialize the entry as being single
        if key not in Id2MarrStatus:
            Id2MarrStatus[key] = {"MARR": [], "DIV": [], "WIDOWER": [], "DEAT": [], "Status": 'Single'}

        # check if this person is dead - if so, then are not married, divorce or single
        if "DEAT" in ind:
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
    for key in ["MARR", "DIV", "HUSB", "WIFE", "CHIL"]:
        if key not in fam or type(fam[key]) is not list:
            fam[key] = []

    return fam


def normalize_ind_entry(i_ind):
    """
    Normalizes all arrays in indily entry
    :param indily: The indily object
    :return: all the keys that take arrays are arrays
    """
    ind = i_ind.copy()
    for key in ["BIRT", "DEAT"]:
        if key not in ind or type(ind[key]) is not list:
            ind[key] = []


def check_dates(dt1, dt2, span, units, upcoming=False):
    """
    check_dates: check if all the dates are within the specified range
                 This routine was based on CS555W class notes provided by Professor Rowland
                 It was adapted to support upcoming dates also.

                 dt1, dt2: 2 datetime dates are passed in (no time units should be passed, optimally).
                 span: range that the 2 dates must fall within
                 units: indicator if checking days, months or years
    :param dt1, dt2, span, units, upcoming
    :returns returns true or false depending if the dates are in range
    """
    dtMap = {"days": 1, "months": 30.4, "years": 365.25}

    if units not in dtMap:
        return False

    dt_diff = (dt1-dt2).days
    if upcoming is True:
        return (dt_diff/dtMap[units] >= 0 and dt_diff/dtMap[units] <= span)
    else:
        return (abs(dt_diff)/dtMap[units] <= span)


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


def datetime_from_date_array(date):
    """
    Converts the GEDCOM array of [day, month, year] to a date time
    :param date: Array of integers in format [day, month, year]
    :return: The datetime object of that array
    """
    return datetime.datetime(date[2], date[1], date[0])


def is_n_days_after(dictionary, field, days=30, from_date=datetime.datetime.today()):
    """
    Takes a date array inside of the dictionary under a specific key, and checks if the other date is days away from
    the provided date
    :param dictionary: The dictionary to source the date form, must contain the key specified in field
    :param field: The key to read from the dictionary
    :param days: The days to check backwards, inclusive
    :param from_date: The date to start the search from, must be a date time object
    :raise TypeError if from_date is not a datetime object
    :return: True if the date is in the range, false otherwise
    """
    try:
        birthday = datetime_from_date_array(dictionary[field])
    except (KeyError, ValueError, AttributeError):
        return False

    month_ago = from_date - datetime.timedelta(days)
    # Todo, validate the year being included is correct
    return month_ago <= birthday <= from_date
