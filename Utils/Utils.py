from collections import namedtuple
from pprint import pprint

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

    latest_marriage=get_latest_date(marriages)
    marriages[0];
    if len(marriages) > 1:
        i=1
        while (i <= len(marriages)):
             # if the year is greater - than greater marriage
             if marriages[i][2]>latest_marriage[2]:
                 latest_marriage=marriages[i]
                 continue

             # if the year is less - break
             if marriages[i][2]<latest_marriage[2]:
                 continue

             # if the month is greater - than greater marriage
             if marriages[i][1]>latest_marriage[1]:
                 latest_marriage=marriages[i]
                 continue

             # if the month is less - break
             if marriages[i][1]<latest_marriage[1]:
                 continue

             # if the day is greater - than continue
             if marriages[i][0]>latest_marriage[0]:
                 latest_marriage=marriages[i]
                 continue

             # if the day is less - break
             if marriages[i][0]<latest_marriage[0]:
                 continue

    latest_marriage=marriages[0];
    return latest_date;

def get_latest_date(dates):
    """
     Return the latest data in an array of dates
    :param List of dates
    :returns the latest date
    """
    #for date in dates:
        #print("Latest Dates: date: {}".format(date))

    latest_date=dates[0]
    if len(dates) > 1:
        i=1
        dlen=len(dates)
        while i < dlen:
             #print("Index i: {}".format(i))
             # if the year is greater - than greater date
             val1=dates[i][2]
             val2=latest_date[2]
             #print("val1: {}, val2:{}".format(val1, val2))
             if val1>val2:
                 latest_date=dates[i]
                 i=i+1;
                 continue

             # if the year is less - break
             if val1<val2:
                 i=i+1;
                 continue

             # the year is the same - look at the month
             # if the month is greater - than greater date
             val1=dates[i][1]
             val2=latest_date[1]
             #print("val1: {}, val2:{}".format(val1, val2))
             if val1>val2:
                 latest_date=dates[i]
                 i=i+1;
                 continue

             # if the month is less - break
             if val1<val2:
                 i=i+1;
                 continue

             # the year and month are the same - look at the day
             # if the day is greater - than continue
             val1=dates[i][0]
             val2=latest_date[0]
             #print("val1: {}, val2:{}".format(val1, val2))
             if val1>val2:
                 latest_date=dates[i]
                 i=i+1;
                 continue

             # if the day is less - break
             if val1<val2:
                 i=i+1;
                 continue

             i=i+1;


    return latest_date


def getMaritalStatus(individuals, families):
    """
     Build a map of person to marriage/divorces
    :param List of Families 
    :returns Map of all IDs to Marriage/Divorces
    """
    Id2MarrStatus={}

    for fam in families:
          
        # look at marriage field
        if ("MARR" in fam) and type(fam["MARR"]) is list:

            # build husband to child mapping
            if ("HUSB" in fam) and type(fam["HUSB"]) is list:
               for husb in fam["HUSB"]:
                   if husb in Id2MarrStatus:
                       Id2MarrStatus[husb]["MARR"].append(fam["MARR"])
                   else:
                       tmp={"MARR":[], "DIV":[]}
                       Id2MarrStatus[husb]=tmp;
                       Id2MarrStatus[husb]["MARR"].append(fam["MARR"])

            # build wife to child mapping
            if ("WIFE" in fam) and type(fam["WIFE"]) is list:
               for wife in fam["WIFE"]:
                   if wife in Id2MarrStatus:
                       Id2MarrStatus[wife]["MARR"].append(fam["MARR"])
                   else:
                       tmp={"MARR":[], "DIV":[]}
                       Id2MarrStatus[wife]=tmp
                       Id2MarrStatus[wife]["MARR"].append(fam["MARR"])

        #look at DIV field
        if ("DIV" in fam) and type(fam["DIV"]) is list:

            # build husband to child mapping
            if ("HUSB" in fam) and type(fam["HUSB"]) is list:
               for husb in fam["HUSB"]:
                   if husb in Id2MarrStatus:
                       Id2MarrStatus[husb]["DIV"].append(fam["DIV"])
                   else:
                       tmp={"DIV":[], "DIV":[]}
                       Id2MarrStatus[husb]=tmp
                       Id2MarrStatus[husb]["DIV"].append(fam["DIV"])

            # build wife to child mapping
            if ("WIFE" in fam) and type(fam["WIFE"]) is list:
               for wife in fam["WIFE"]:
                   if wife in Id2MarrStatus:
                       Id2MarrStatus[wife]["DIV"].append(fam["DIV"])
                   else:
                       tmp={"MARR":[], "DIV":[]}
                       Id2MarrStatus[wife]=tmp
                       Id2MarrStatus[wife]["DIV"].append(fam["DIV"])


    for ind in individuals:
        if ind["INDI"] in Id2MarrStatus:
            # then  this person has been either married or divorced
            marriages=Id2MarrStatus[ind["INDI"]]["MARR"]
            divorces=Id2MarrStatus[ind["INDI"]]["DIV"]
            if len(divorces)==0:
                Id2MarrStatus[ind["INDI"]]["Status"]="Married"
            else:
                latest_marriage=get_latest_date(marriages)
                latest_divorce=get_latest_date(divorces)
                if latest_marriage[2]>latest_divorce[2]:
                    Id2MarrStatus[ind["INDI"]]["Status"]="Married"
                    continue

                if latest_marriage[2]<latest_divorce[2]:
                    Id2MarrStatus[ind["INDI"]]["Status"]="Divorced"
                    continue

                # the year is the same - look at the month
                if latest_marriage[1]>latest_divorce[1]:
                    Id2MarrStatus[ind["INDI"]]["Status"]="Married"
                    continue;

                if latest_marriage[1]<latest_divorce[1]:
                    Id2MarrStatus[ind["INDI"]]["Status"]="Divorced"
                    continue;

                # the year and day are the same - look at the day
                if latest_marriage[0]>latest_divorce[0]:
                    Id2MarrStatus[ind["INDI"]]["Status"]="Married"
                    continue;

                Id2MarrStatus[ind["INDI"]]["Status"]="Divorced"

        else: # else the person was never married
            tmp={"MARR":[], "DIV":[], "Status":"Single"}
            Id2MarrStatus[ind["INDI"]]=tmp


    return Id2MarrStatus

