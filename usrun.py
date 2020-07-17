# The UserStory program by developer&tester Chengyi Zhang
from collections import defaultdict, Counter
from Utils.Logger import Logger
import datetime
from typing import List

logger = Logger()


# tools

def IDtoINDI(individuals_from_db) -> dict:
    ans = dict()
    for one in individuals_from_db:
        ans.setdefault(one['INDI'], one)
    return ans


months = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG',
          9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}


def IDinFam(families_from_db) -> dict:
    ans = defaultdict(list)
    for fam in families_from_db:
        if fam['HUSB'] != '-':
            for one in fam['HUSB']:
                ans[one].append(fam)
        if fam['WIFE'] != '-':
            for one in fam['WIFE']:
                ans[one].append(fam)
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
            for i in range(l - 1):
                for j in range(i + 1, l):
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
        if 'CHIL' in fam and type(fam['CHIL']) is not str:
            for id in fam['CHIL']:
                one = id_indi[id]
                if ('BIRT' in one):
                    date = str(one['BIRT'][0]) + '/' + str(one['BIRT'][1]) + '/' + str(one['BIRT'][2])
                    ib.setdefault(date, [])
                    ib[date].append(one['INDI'])
        for birth, ids in ib.items():
            if (len(ids) > 1):
                ret.append((birth, fam['FAM'], ids))
    return ret


# End of Sprint 1

# Sprint 2

# US38 Upcoming Birthdays

def us38(families_from_db, individuals_from_db):
    ret = upcoming_birthdays(individuals_from_db)
    for indiid, date in ret:
        logger.log_individual_info(38, "Individual {}'s birthday {} is coming soon"
                                   .format(indiid, date))


def upcoming_birthdays(individuals_from_db):
    ret = []
    for one in individuals_from_db:
        current_date = datetime.datetime.today()
        if current_date.month == 12 and current_date.day > 1:
            try:
                date = datetime.datetime(current_date.year + 1, one['BIRT'][1], one['BIRT'][0])
            except:
                continue
        else:
            try:
                date = datetime.datetime(current_date.year, one['BIRT'][1], one['BIRT'][0])
            except:
                continue
        if datetime.timedelta(days=0) < date - current_date < datetime.timedelta(days=30):
            ret.append((one['INDI'], months[one['BIRT'][1]] + ' ' + str(one['BIRT'][0])))
    return ret


# US11 Bigamy

def us11(families_from_db, individuals_from_db):
    ret = no_bigamy_one_fam(families_from_db, individuals_from_db)
    for one in ret:
        logger.log_family_error(11, "Family {} has more than 2 spouses".format(one))

    ret = no_bigamy_sev_fam(families_from_db, individuals_from_db)
    for one in ret:
        logger.log_individual_error(11, "Individual {} has more than 1 spouse at the same time".format(one))


def no_bigamy_one_fam(families_from_db, individuals_from_db):
    ret = []
    for fam in families_from_db:
        nh = len(fam['HUSB']) if fam['HUSB'][0] != '-' else 0
        nw = len(fam['WIFE']) if fam['WIFE'][0] != '-' else 0
        if nh + nw > 2:
            ret.append(fam['FAM'])
    return ret


def no_bigamy_sev_fam(families_from_db, individuals_from_db):
    ret = set()
    d = defaultdict(list)
    for fam in families_from_db:
        nh = len(fam['HUSB']) if fam['HUSB'][0] != '-' else 0
        nw = len(fam['WIFE']) if fam['WIFE'][0] != '-' else 0
        if nh + nw > 2 or nh + nw == 1:
            continue
        couple = []
        if (nh == 1 and nw == 1):
            couple.append(fam['HUSB'][0])
            couple.append(fam['WIFE'][0])
        if (nh == 0):
            couple = fam['WIFE'].copy()
        if (nw == 0):
            couple = fam['HUSB'].copy()
        d[couple[0]].append((fam["MARR"], couple[1], fam))
        d[couple[1]].append((fam["MARR"], couple[0], fam))
    for one, lst in d.items():
        dates = []
        for marriage, spouseid, fam in lst:
            dates.append((spouseid, datetime.datetime(marriage[2], marriage[1], marriage[0]), True))
            spouse = IDtoINDI(individuals_from_db)[spouseid]
            if ('DEAT' in spouse):
                dates.append(
                    (fam['FAM'], datetime.datetime(spouse['DEAT'][2], spouse['DEAT'][1], spouse['DEAT'][0]), False))
            elif ('DIV' in fam):
                dates.append((fam['FAM'], datetime.datetime(fam['DIV'][2], fam['DIV'][1], fam['DIV'][0]), False))
        dates.sort(key=lambda x: x[1])
        havespouse = False
        for fid, date, factor in dates:
            if (factor):
                if (havespouse):
                    ret.add(one)
                else:
                    havespouse = True
            else:
                havespouse = False
    return sorted(list(ret))


# End of Sprint 2

# Sprint 3

def us12(families_from_db, individuals_from_db):
    ret = parents_not_too_old(families_from_db, individuals_from_db)
    for gen, parent, parentid, child, negative in ret:
        logger.log_family_error(12, "{} {} is too old compared to {} child {}"
                                    .format(parent, parentid, gen, child + negative))


def parents_not_too_old(families_from_db, individuals_from_db):
    ret = []
    id_indi = IDtoINDI(individuals_from_db)
    for fam in families_from_db:
        if 'CHIL' in fam:
            for one in fam['CHIL']:
                child = id_indi[one]
                if fam['HUSB'] != '-':
                    for father in fam['HUSB']:
                        if id_indi[father]['AGE'] - child['AGE'] > 80:
                            ret.append(('his', 'Father', father, one, ", while age of the child is negative" if child['AGE'] < 0 else ""))
                if fam['WIFE'] != '-':
                    for mother in fam['WIFE']:
                        if id_indi[mother]['AGE'] - child['AGE'] > 60:
                            ret.append(('her', 'Mother', mother, one, ", while age of the child is negative" if child['AGE'] < 0 else ""))
    return ret


def us19(families_from_db, individuals_from_db):
    ret = first_cousin_not_marry(families_from_db, individuals_from_db)
    for a, b in ret:
        logger.log_family_error(19, "Couple {} and {} are first cousins".format(a, b))


def first_cousin_not_marry(families_from_db, individuals_from_db):
    ret = []
    id_fam = IDinFam(families_from_db)
    for fam in families_from_db:
        if "CHIL" in fam and len(fam["CHIL"]) > 1:
            cousins: List[List[str]] = []
            for one in fam['CHIL']:
                children = []
                if one in id_fam:
                    for ano in id_fam[one]:
                        if 'CHIL' in ano:
                            children.extend(ano['CHIL'])
                cousins.append(children)
            # check all pairs of cousins
            for a in range(len(cousins)):
                for b in range(a+1, len(cousins)):
                    for x in cousins[a]:
                        for y in cousins[b]:
                            if x in id_fam and y in id_fam:
                                if len([n for n in id_fam[x] if n in id_fam[y]]) > 0:
                                    ret.append((x, y))
    return ret

# End of Sprint 3
