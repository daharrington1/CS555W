from collections import namedtuple

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



    """
     Checks for Families where a spouse is married to a child

    :param Families collection in the database
    :returns List of Familes that have a spouse married to a child
    """
def us17_no_marr2child(famObj):
        #Call database to get all families with marriages to children
            return famObj.getMarriagestoChildren()




def us16_male_last_names(individuals, families):
    male_lastnames = []  # list of suspect families
    id2Name={}           # mapping of male ids to last name

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
    
