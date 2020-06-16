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


def us17_no_marr2childa(individuals=None, families=None):
     """
     Checks for Families where a spouse is married to a child

     :param Families collection in the database
     :returns List of Familes that have a spouse married to a child
     """
     if (individuals == None) or (families == None):
        print("Inputs are missing")
        raise Exception(ValueError, "Missing Inputs")


     ret= []  # list of suspect families
     parentId2Children=getParent2ChildrenMap(families)  #create a map of all parents to children

     for fam in families:
         # get all husband/wives in the family and check to see if their spouse is their child
         spouses=getSpousesInFamily(fam)
         for spouse in spouses:
             mySpouses=getMySpouse(spouse, fam) # just in case you have more than one spouse
             for myspouse in mySpouses:
                 #get all my children and check if spouse is in them
                 if spouse in parentId2Children:
                     children=parentId2Children[spouse]
                     if myspouse in children:
                         #my spouse is married to my child
                         tmp={"Spouse":spouse, "MySpouse":myspouse, "FAM":fam["FAM"], "MyChildren":children}
                         ret.append(tmp)
     #return all matches
     return ret


def us16_male_last_names(individuals, families):
    male_lastnames = []  # list of suspect families
    id2Name={}           # mapping of male ids to last name

    if (individuals == None) or (families == None):
        print("Inputs are missing")
        raise Exception(ValueError, "Missing Inputs")

    # build map of id to mail last names
    for ind in individuals:
        if ind["SEX"]=="M":  # only store male names
            id2Name[ind["INDI"]]=ind["NAME"].split("/")[1]

    for fam in families:
        lastNames=[]

        # assume it is a bad family at first
        badFam={"FAM":fam["FAM"]}

        # look at husbands last names
        if ("HUSB" in fam) and type(fam["HUSB"]) is list:

            for male in fam["HUSB"]:
                if male not in id2Name:
                    raise Exception(ValueError, "Husband {} is not in the male mapping".format(male))

                if id2Name[male] not in lastNames:
                   lastNames.append(id2Name[male])

        # look at male children last names
        if ("CHIL" in fam) and type(fam["CHIL"]) is list:
            for child in fam["CHIL"]:
                # only look at males and non-unique last names
                if child in id2Name and id2Name[child] not in lastNames:  
                      lastNames.append(id2Name[child])

        #check for unique male last names in families
        if len(lastNames) > 1:
            badFam["LNAMES"]=lastNames
            male_lastnames.append(badFam)


    return male_lastnames;
    

