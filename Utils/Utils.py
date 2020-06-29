from collections import namedtuple
from pprint import pprint
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


def getIdMap(records):
    """
     Build a map of id to their record
    :param List of either Individuals and Families from the database
    :returns Map of all IDs to record
    """
    idMap = dict()
    for record in records:
        if "INDI" in record:
            idMap.setdefault(record['INDI'], record)
        if "FAM" in record:
            idMap.setdefault(record['FAM'], record)

    return idMap;


def getDateTimestamp(date):
    """
     Convert the array date value to a date timestamp
    :param Single Date in an array
    :returns Timestamp of the date
    """
    if date==[] or date=='':
        return 0;

    # convert to timestamp - inputs: year/month/date
    date_timestamp =  datetime.datetime(date[2], date[1], date[0]).timestamp()
    return date_timestamp


def getParent2ChildrenMap(families):
    """
     Build a map of parent to children - crosses families if married more than once
    :param List of Individuals and Families 
    :returns Map of all Parent IDs to Children
    """
    parentId2Children={}

    for fam in families:

        #don't need to do anything if there's no children
        if ("CHIL" in fam) and type(fam["CHIL"]) is list:

            #add child to parent id mapping
            for child in fam["CHIL"]:
                # build husband parent to child mapping
                if ("HUSB" in fam) and type(fam["HUSB"]) is list:
                    for husb in fam["HUSB"]:
                        if husb in parentId2Children:
                            if child not in parentId2Children[husb]:
                                parentId2Children[husb].append(child)
                        else:
                            parentId2Children[husb]=[]
                            parentId2Children[husb].append(child)

                # build husband parent to child mapping
                if ("WIFE" in fam) and type(fam["WIFE"]) is list:
                    for wife in fam["WIFE"]:
                        if wife in parentId2Children:
                            if child not in parentId2Children[wife]:
                                parentId2Children[wife].append(child)
                        else:
                            parentId2Children[wife]=[child]

    return parentId2Children;


def getMySpouse(id, fam):
    """
     Figure out My Spouse in the current family
    :param a single family
    :returns my spouse in the given family
    """
    #check if there is a wife field

    Spouses=[]

    if ("WIFE" in fam) and type(fam["WIFE"]) is list:
        #if not same sex marriage - your spouse is in the husband field - or there is no spouse
        if id in fam["WIFE"] and len(fam["WIFE"])==1:
            if "HUSB" in fam and type(fam["HUSB"]) is list:
                Spouses=fam["HUSB"]
        else:
            #get all spouses in the wife list that aren't input id
            for wid in fam["WIFE"]:
                if id != wid:
                    Spouses.append(wid)
    else:
         #there is no wife - so both spouses are in the HUSB list or there is no spouse
         #if I'm the first WIFE, my spouse is the second
         for wid in fam["HUSB"]:
             if id != wid:
                Spouses.append(wid)

    return Spouses


def getSpousesInFamily(fam):
    """
     Return spouses in a single family in one array

    :param a single family
    :returns array of the spouses 
    """

    Spouses=[]

    if ("WIFE" in fam) and type(fam["WIFE"]) is list:
        #if not same sex marriage - your spouse is in the husband field - or there is no spouse
        for wife in fam["WIFE"]:
            if wife not in Spouses:
                Spouses.append(wife)

    if ("HUSB" in fam) and type(fam["HUSB"]) is list:
        #if not same sex marriage - your spouse is in the husband field - or there is no spouse
        for husb in fam["HUSB"]:
            if husb not in Spouses:
                Spouses.append(husb)

    return Spouses


def getLatestDate(dates):
    """
     Return the latest data in an array of dates
    :param List of dates
    :returns the latest date
    """
    #for date in dates:
        #print("Latest Dates: date: {}".format(date))
    if len(dates) < 1:
       return []

    latest_date=getDateTimestamp(dates[0])
    latest_date_val=dates[0]

    if len(dates) > 1:
        i=1
        dlen=len(dates)
        while i < dlen:
             date=getDateTimestamp(dates[i])
             if date <= latest_date:
                 i=i+1
                 continue;
             else:
                 latest_date=date
                 latest_date_val=dates[i]

             i=i+1

    return latest_date_val


def getMaritalStatus(individuals, families):
    """
     Build a map of person to marriage/divorces
    :param List of Families 
    :returns Map of all IDs to Marriage/Divorces
    """
    # get map of ID to individual information
    indMap=getIdMap(individuals)
    Id2MarrStatus={}


    # build a map of marriages and divorces for each spouse in a family
    for fam in families:
        # check for single parent 
        if ("WIFE" in fam and type(fam["WIFE"]) is list and len(fam["WIFE"])==1):
            if ("HUSB" in fam and type(fam["HUSB"]) is not list and fam["HUSB"]=="-"):
                # they are single parent and not married, divorced or widower
                continue;

        # check for single parent 
        if ("HUSB" in fam and type(fam["HUSB"]) is list and len(fam["HUSB"])==1):
            if ("WIFE" in fam and type(fam["WIFE"]) is not list and fam["WIFE"]=="-"):
                # they are single parent and not married, divorced or widower
                continue;

        for spouse in ["HUSB", "WIFE"]:  # loop through the spouses
            if (spouse in fam) and type(fam[spouse]) is list:
                for person in fam[spouse]:
                    if person not in Id2MarrStatus:
                        Id2MarrStatus[person]={"MARR":[], "DIV":[], "WIDOWER":[], "Status": ''}

                    # If there is a divorce date - then you can't still be married or a widower to this person
                    if "DIV" in fam and type(fam["DIV"]) is list:
                        Id2MarrStatus[person]["DIV"].append(fam["DIV"]) # append the date
                        continue;

                    # you are married or a widower
                    if "MARR" in fam and type(fam["MARR"]) is list:
                        my_spouses=getMySpouse(person, fam)
                        marriage_date=fam["MARR"]
                        for my_spouse in my_spouses:
                            # at this point you are either still married to spouse or windower
                            if "DEAT" in indMap[my_spouse] and type(indMap[my_spouse]["DEAT"]) is list:
                               Id2MarrStatus[person]["WIDOWER"].append(indMap[my_spouse]["DEAT"])
                            else:
                               # if you are not a widower, then you are still married to this person
                               Id2MarrStatus[person]["MARR"].append(marriage_date)



    for ind in individuals:

        # check if this person is dead - if so, then are not married, divorce or single
        if "DEAT" in ind and type(ind["DEAT"]) is list:
           if ind["INDI"] in Id2MarrStatus:
               Id2MarrStatus[ind["INDI"]]["Status"]="Dead";
           else:
               Id2MarrStatus[ind["INDI"]]={"MARR":[], "DIV":[], "WIDOWER":[], "Status": 'Dead'}
           continue;

        # check if they are married
        if ind["INDI"] in Id2MarrStatus:
            # then  this person has been either married or divorced or widowed
            #print("\n\nId2MarrStatus: {}".format(Id2MarrStatus[ind["INDI"]]))
            if Id2MarrStatus[ind["INDI"]]["Status"]=="Dead":
                continue

            # look at all the non dead people
            latest_widower = getLatestDate(Id2MarrStatus[ind["INDI"]]["WIDOWER"])
            latest_marriage= getLatestDate(Id2MarrStatus[ind["INDI"]]["MARR"])
            latest_divorce= getLatestDate(Id2MarrStatus[ind["INDI"]]["DIV"])
            #print("++++++++++Individual {}: latest_widower: {}, latest_marriage: {}, latest_divorce: {}".format(ind["INDI"], latest_widower, latest_marriage, latest_divorce))

            latest_widower_timestamp = getDateTimestamp(latest_widower)
            latest_marriage_timestamp = getDateTimestamp(latest_marriage)
            latest_divorce_timestamp= getDateTimestamp(latest_divorce)

            if latest_widower_timestamp==0:
                if latest_divorce_timestamp==0:
                    Id2MarrStatus[ind["INDI"]]["Status"]="Married"
                else:
                    if latest_divorce_timestamp>=latest_marriage_timestamp:
                        Id2MarrStatus[ind["INDI"]]["Status"]="Divorced"
                    else:
                        Id2MarrStatus[ind["INDI"]]["Status"]="Married"
            else: # at least one of your spouses died
                if latest_widower_timestamp>=latest_divorce_timestamp and latest_widower_timestamp>=latest_marriage_timestamp:
                        Id2MarrStatus[ind["INDI"]]["Status"]="Widower"
                else:
                    if latest_divorce_timestamp>=latest_marriage_timestamp:
                        Id2MarrStatus[ind["INDI"]]["Status"]="Divorced"
                    else:
                        Id2MarrStatus[ind["INDI"]]["Status"]="Married"
        else: # else the person was never married
            Id2MarrStatus[ind["INDI"]]={"MARR":[], "DIV":[], "Status":"Single"}


    return Id2MarrStatus


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
