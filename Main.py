from Parser.parserV4 import parser4
from db.db_interface import GenComDb
from TablePrinter.TablePrinter import TablePrinter
import Utils

# Get a reference to the collection, and clear out previous data, assuming desired behavior is always to read from file
individual_database = GenComDb(GenComDb.MONGO_INDIVIDUALS)
family_database = GenComDb(GenComDb.MONGO_FAMILIES)
individual_database.dropCollection()
family_database.dropCollection()

#parsed_individuals, parsed_families = raw2dic("ModernFamilyTest.ged")
new_parser = parser4("ModernFamilyTest.txt")
parsed_individuals = new_parser.indi_dic
parsed_families = new_parser.fam_dic

# Input all the users
# Maps the age from all users, based on the current date the program is ran if no death is specified
# US07: validate the age, less than 150, at the same time. Errors should be print out
new_parser.add_valid_age()
# US01: check dates are not before current date
new_parser.dateCheck()

for parsed_individual_id in parsed_individuals:
    # Grab the individual and insert their id into the dictionary, for the database to use as its primary key
    individual = parsed_individuals[parsed_individual_id]

    individual["INDI"] = parsed_individual_id
    individual_database.AddObj(individual)

# These loops can be consolidated after debugging needs are done
for family_id in parsed_families:
    family = parsed_families[family_id]
    family["FAM"] = family_id

    # Error handling to fill in required fields which are not present in one or more families
    # Placeholder logic to Proof-of-concept all the branches working together
    if "MARR" not in family:
        print("Error: Family {}  missing required tag marr".format(family_id))
        family["MARR"] = TablePrinter.error_output
    if "WIFE" not in family:
        print("Error: Family {} missing wife".format(family_id))
        family["WIFE"] = TablePrinter.error_output

    if "HUSB" not in family:
        print("Error: Family {} missing husb".format(family_id))
        family["HUSB"] = TablePrinter.error_output

    family_database.AddObj(family)

# Read the data back out from the DB
individuals_from_db = []
all_ids = individual_database.getAllIds()
for individual_id in all_ids:
    individuals_from_db.append(individual_database.getDoc(individual_id["INDI"]))

families_from_db = []
all_families = family_database.getAllIds()
for family_id in all_families:
    families_from_db.append(family_database.getDoc(family_id["FAM"]))

# Output the data
printer = TablePrinter(individual_database)
print(printer.format_individuals(individuals_from_db))
print(printer.format_individuals(individual_database.getDeadAsList(), TablePrinter.table_label_dead_individual))
print(printer.format_families(families_from_db))

non_uniques = Utils.filter_non_unique_individuals(individuals_from_db)
if len(non_uniques) > 0:
    output = "Individuals with the same name and birth date:\n"
    for conflict in non_uniques.values():
        output += "\tFor Name: {} and Date: {} \n".format(conflict[0].name, printer.format_date(conflict[0].birthday))
        output += "\t\t- {}\n".format(",".join([id.id for id in conflict]))
    print(output)
else:
    print("All individuals are unique in the file, by name and birth date")


# Check for any parents married to children
ret=Utils.us17_no_marr2child(family_database)
if len(ret)==0:
    print("No spouses in families are married to children")
else:
    for fam in ret:
        print("Family ({}) has marriages to children: husband({}), wife({}), children({})".format(fam["FAM"], fam["HUSB"], fam["WIFE"], fam["CHIL"]))
