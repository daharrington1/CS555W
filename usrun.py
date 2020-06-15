# The UserStory program by developer&tester Chengyi Zhang

from Main import individuals_from_db, families_from_db

# US24 List Children with Divorced Parents
for family in families_from_db:
    if('DIV' in family):
        if('CHIL' in family):
            for one in family['CHIL']:
                for p in individuals_from_db:
                    if(p['INDI'] == one):
                        print("ANOMALY: Child " + p['NAME'] + " has divorced parents")

# US32 List People Having the Same Birthday
bds = dict()
for one in individuals_from_db:
    t = bds.get(one['BIRT'],[])
    bds[one['BIRT']].append(one['NAME'])
for date, names  in bds.items():
    if(len(names)>1):
        print("ANOMALY: " + ' and '.join(names) + " have the same birthday")


'''
TEMPORARY
print(individuals_from_db[0])
print(families_from_db[0])
'''

