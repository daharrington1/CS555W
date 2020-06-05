from Parser.parser import raw2dic
from db.db_interface import GenComDb
from TablePrinter.TablePrinter import TablePrinter

# Get a reference to the collection, and clear out previous data, assuming desired behavior is always to read from file
individual_database = GenComDb(GenComDb.MONGO_INDIVIDUALS)
family_database = GenComDb(GenComDb.MONGO_FAMILIES)
individual_database.dropCollection()
family_database.dropCollection()

parsed_data = raw2dic("ModernFamily.ged")

# Input all the users
parsed_individuals = parsed_data[0]
for parsed_individual_id in parsed_individuals:
    # Grab the individual and insert their id into the dictionary, for the database to use as its primary key
    individual = parsed_individuals[parsed_individual_id]
    individual["INDI"] = parsed_individual_id
    individual_database.AddObj(individual)

# These loops can be consolidated after debugging needs are done
parsed_families = parsed_data[1]
for family_id in parsed_families:
    family = parsed_families[family_id]
    family["FAM"] = family_id

    # Error handling to fill in required fields which are not present in one or more families
    # Placeholder logic to Proof-of-concept all the branches working together
    if "MARR" not in family:
        print("Error: Family missing required tag")
        family["MARR"] = "ERR"
    if "WIFE" not in family:
        print("Error: Family missing wife")
        family["WIFE"] = "ERR"

    if "HUSB" not in family:
        print("Error: Family missing husb")
        family["HUSB"] = "ERR"

    family_database.AddObj(family)

individual_database.my_collection()


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
printer.print_individuals(individuals_from_db)
printer.print_families(families_from_db)
