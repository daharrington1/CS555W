# The UserStory program by developer&tester Chengyi Zhang
from Utils.Logger import Logger

logger = Logger()


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
        logger.log_family_error(24,
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
                    if (len(spouss[i].intersection(spouss[j])) == len(spouss[i])):
                        ret.append((date, famids[i], famids[j]))
    return ret


# US32 Multiple Births
def us32(families_from_db, individuals_from_db):
    ret = multiple_births(families_from_db, individuals_from_db)
    for birth, famid, indiid in ret:
        logger.log_family_warning(32, "Family {} has children {} with the same birthday {}"
                                .format(famid, ', '.join(indiid[:-1]) + ' and ' + indiid[-1], birth))


def multiple_births(families_from_db, individuals_from_db):
    ret = []
    id_indi = IDtoINDI(individuals_from_db)
    for fam in families_from_db:
        # individual_birthday
        ib = dict()
        if('CHIL' in fam and type(fam['CHIL']) is not str):
            for id in fam['CHIL']:
                one = id_indi[id]
                if('BIRT' in one):
                    date = str(one['BIRT'][0]) + '/' + str(one['BIRT'][1]) + '/' + str(one['BIRT'][2])
                    ib.setdefault(date, [])
                    ib[date].append(one['INDI'])
        for birth, ids in ib.items():
            if(len(ids) > 1):
                ret.append((birth, fam['FAM'], ids))
    return ret


'''
TEMPORARY
print(individuals_from_db[0])
print(families_from_db[0])
'''
