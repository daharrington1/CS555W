# The UserStory program by developer&tester Chengyi Zhang

# tool
def IDtoINDI(individuals_from_db):
    ans = dict()
    for one in individuals_from_db:
        ans.setdefault(one['INDI'], one)
    return ans


# US24 List Children with Divorced Parents
def children_parents_divorced(families_from_db, individuals_from_db):
    id_indi = IDtoINDI(individuals_from_db)
    for family in families_from_db:
        if ('DIV' in family):
            if ('CHIL' in family):
                for one in family['CHIL']:
                    print("ANOMALY: INDIVIDUAL: Child " + id_indi[one]['NAME'] + " has divorced parents")


# US32 List People Having the Same Birthday
def people_same_birthday(individuals_from_db):
    bds = dict()
    for one in individuals_from_db:
        s = str(one['BIRT'][0]) + '/' + str(one['BIRT'][1]) + '/' + str(one['BIRT'][2])
        n = one['NAME']
        bds.setdefault(s, [])
        bds[s].append(n)
    for date, names in bds.items():
        if len(names) > 1:
            print("ANOMALY: INDIVIDUAL: " + ', '.join(names[:-1]) + ', and ' +
                  names[-1] + " have the same birthday " + date)


'''
TEMPORARY
print(individuals_from_db[0])
print(families_from_db[0])
'''
