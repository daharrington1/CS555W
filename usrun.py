# The UserStory program by developer&tester Chengyi Zhang
from Utils.Logger import Logger


# tool
def IDtoINDI(individuals_from_db):
    ans = dict()
    for one in individuals_from_db:
        ans.setdefault(one['INDI'], one)
    return ans


# US24 Unique Families by spouses
def us24(families_from_db, individuals_from_db):
    ret = unique_families(families_from_db, individuals_from_db)
    for date, a, b in ret:
        Logger.log_family_error(24,
                                "Family {} and Family {} share the same spouses by name and marriage date {}".format(a,
                                                                                                                     b,
                                                                                                                     date))


def unique_families(families_from_db, individuals_from_db):
    id_indi = IDtoINDI(individuals_from_db)
    ret = []
    # the dict of families keyword by marriage date
    df = dict()
    for fam in families_from_db:
        if ("MARR" in fam and type(fam["MARR"] is list) and type(fam["MARR"]) is not str):
            date = str(fam['MARR'][0]) + '/' + str(fam['MARR'][1]) + '/' + str(fam['MARR'][2])
            df.setdefault(date, [])
            spouses = set()
            if ('HUSB' in fam and type(fam['HUSB']) is list):
                for one in fam['HUSB']:
                    spouses.add(id_indi[one]["NAME"])
            if ('WIFE' in fam and type(fam['WIFE']) is list):
                for one in fam['WIFE']:
                    spouses.add(id_indi[one]["NAME"])
            df[date].append((spouses, fam["FAM"]))
    for date, value in df.items():
        spouss = []
        famids = []
        for f, s in value:
            spouss.append(f)
            famids.append(s)
        l = len(spouss)
        if (l > 1):
            for i in range(l-1):
                for j in range(i+1, l):
                    if (len(spouss[i].intersect(spouss[j])) == len(spouss[i])):
                        ret.append((date, famids[i], famids[j]))
    return ret


# US32 List People Having the Same Birthday
def us32(individuals_from_db):
    ret = multiple_births(individuals_from_db)
    for dates, ID in ret:
        Logger.log_family_error(24, "Individual {} has more than one birthday: {}"
                                .format(ID, dates))

def multiple_births(individuals_from_db):
    ret = []
    ib = dict()
    for one in individuals_from_db:
        ib.setdefault(one['INDI'], [])
        ib[one['INDI']].append(one['BIRT'])
    for id, birts in ib.items():
        if(len(birts)>1):
            ret.append((', '.join(birts[:-1]) + ', and ' + birts[-1], id))
    return ret


'''
TEMPORARY
print(individuals_from_db[0])
print(families_from_db[0])
'''
