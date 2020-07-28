from Parser.parser_checker import parser4
from db.db_interface import GenComDb
from TablePrinter.TablePrinter import TablePrinter
from Utils import Utils
from Utils.Logger import Logger
from Utils import UserStory30, UserStory31
from Utils.Utils import normalize_family_entry, getParent2ChildrenMap
import usrun
from Utils.UserStory33 import find_all_orphans
from Utils.DateValidator import DateValidator, format_date
from Utils.UserStory21 import find_mistitled_spouse
from Utils.UserStory13 import find_invalid_sibling_spacing
from Utils.indiDateChecker import indiDateChecker
from Utils.spouseCrossChecker import spouseCrossChecker
from Utils.UserStory28 import sort_children_by_age
from Utils.UserStory35 import born_within_one_month

logger = Logger()
dateValidator = DateValidator(logger)

# Get a reference to the collection, and clear out previous data, assuming desired behavior is always to read from file
individual_database = GenComDb(GenComDb.MONGO_INDIVIDUALS)
family_database = GenComDb(GenComDb.MONGO_FAMILIES)
individual_database.dropCollection()
family_database.dropCollection()

# parsed_individuals, parsed_families = raw2dic("ModernFamilyTest.ged")
new_parser = parser4("ModernFamilyTest.ged", logger)
parsed_individuals = new_parser.indi_dic
parsed_families = new_parser.fam_dic

# Input all the users
# Maps the age from all users, based on the current date the program is ran if no death is specified
# US07: validate the age, less than 150, at the same time. Errors should be print out
new_parser.add_valid_age()
# US01: check dates are not before current date
new_parser.dateCheck()
indiDatechecker = indiDateChecker(logger)

for parsed_individual_id in parsed_individuals:
    # Grab the individual and insert their id into the dictionary, for the database to use as its primary key
    individual = parsed_individuals[parsed_individual_id]

    individual["INDI"] = parsed_individual_id
    individual_database.AddObj(individual)

    indiDatechecker.us03_birtBeforeDeat(individual)
    indiDatechecker.us38_upcomingBirt(individual)

    if born_within_one_month(individual):
        logger.log_individual_info(35, "{} Was born in the last 30 days!".format(parsed_individual_id))

    for key in [key for key in ["BIRT", "DEAT"] if key in individual]:
        dateValidator.validate_date(individual[key], True)

# get the map of siblings
parentId2Children = getParent2ChildrenMap(parsed_families)

for family_id in parsed_families:
    family = parsed_families[family_id]
    family["FAM"] = family_id

    # Error handling to fill in required fields which are not present in one or more families
    # Placeholder logic to Proof-of-concept all the branches working together
    if "MARR" not in family:
        logger.log_family_error(0, "Family {}  missing required tag MARR".format(family_id))
        family["MARR"] = TablePrinter.error_output
    if "WIFE" not in family:
        logger.log_family_error(0, "Family {} missing wife".format(family_id).format(family_id))
        family["WIFE"] = TablePrinter.error_output

    if "HUSB" not in family:
        logger.log_family_error(0, "Family {} missing HUSB".format(family_id))
        family["HUSB"] = TablePrinter.error_output

    family_database.AddObj(family)

    spousecheck = spouseCrossChecker(logger, family, parsed_individuals)
    spousecheck.us02_marrBeforeBirt()
    spousecheck.us05_marrBeforeDeat()
    spousecheck.us06_divBeforeDeat()
    spousecheck.us10_marrAfter14()
    spousecheck.us15_sibling_count()
    spousecheck.us16_male_last_names()
    spousecheck.us17_no_marr2child(parentId2Children)
    spousecheck.us18_no_siblingmarriages(parentId2Children)
    spousecheck.us39_upcoming_anniversaries()
    spousecheck.us14_mult_births()
    spousecheck.us32_mult_births()

    for key in [key for key in ["MARR", "DIV"] if key in family]:
        dateValidator.validate_date(family[key], False)

logger.log_family_info(28, "Children are sorted in order in the Family Table")
# Read the data back out from the DB
individuals_from_db = []
ind_map = {}
all_ids = individual_database.getAllIds()
for individual_id in all_ids:
    rec = individual_database.getDoc(individual_id["INDI"])
    individuals_from_db.append(rec)
    # ind_map[rec["INDI"]]=normalize_ind_entry(rec)
    ind_map[rec["INDI"]] = rec

families_from_db = []
fam_map = {}
all_families = family_database.getAllIds()
for family_id in all_families:
    rec = family_database.getDoc(family_id["FAM"])
    families_from_db.append(rec)
    fam_map[rec["FAM"]] = normalize_family_entry(rec)

# Output the data
printer = TablePrinter(individual_database)
print(printer.format_individuals(individuals_from_db))
print(printer.format_individuals(individual_database.getDeadAsList(), TablePrinter.table_label_dead_individual))
print(printer.format_families(families_from_db))

non_uniques = Utils.filter_non_unique_individuals(individuals_from_db)
if len(non_uniques) > 0:
    for conflict in non_uniques.values():
        formatted = "Same Name & birthday For Name: {} and Date: {} for ids {}" \
            .format(conflict[0].name,
                    format_date(conflict[0].birthday, conflict[0].birthday),
                    ",".join([id.id for id in conflict]))
        logger.log_individual_error(23, formatted)
else:
    logger.log_individual_info(23, "All individuals are unique in the file, by name and birth date")

ret = UserStory30.us30_get_married_individuals(ind_map, fam_map)
if len(ret) > 0:
    logger.log_individual_info(30, "Living Married: {}".format(",".join(sorted(ret))))

ret = UserStory31.us31_get_single_individuals(ind_map, fam_map)
if len(ret) > 0:
    logger.log_individual_info(31, "Living Single: {}".format(",".join(sorted(ret))))

orphans_by_family = find_all_orphans(individuals_from_db, families_from_db)
if len(orphans_by_family) > 0:
    for family_orphan in orphans_by_family:
        # Use the ID to pull the FAMC field, as FAMC will always be a list of size one, and every family will
        # have at least one orphan at if it was included
        family_id = parsed_individuals[family_orphan[0]]["FAMC"][0]
        logger.log_family_anomaly(33, "{} are an orphans in family {}".format(" & ".join(family_orphan), family_id))
else:
    logger.log_family_info(33, "No orphans in file")

mismatched_marriage_roles = find_mistitled_spouse(parsed_individuals, families_from_db)
if len(mismatched_marriage_roles) > 0:
    for mismatched_role in mismatched_marriage_roles:
        logger.log_individual_error(21, "{} is the wrong sex for their listed marriage role ".format(mismatched_role))
else:
    logger.log_individual_info(21, "No mismatched marriage roles in file")

invalid_spaced_siblings = find_invalid_sibling_spacing(parsed_individuals, families_from_db)
if len(invalid_spaced_siblings) > 0:
    for invalid_sibling_id in invalid_spaced_siblings:
        logger.log_individual_anomaly(13, "{} birth is less than 8 months away from a non-twin"
                                      .format(invalid_sibling_id))
else:
    logger.log_family_info(13, "All siblings in all families are twins or spaced more than 8 months apart")

# Chengyi Zhang
# Sprint 1
usrun.us24(families_from_db, individuals_from_db)
# usrun.us32(families_from_db, individuals_from_db)
# Sprint 2
# usrun.us38(families_from_db, individuals_from_db) # refactored by Yikun
usrun.us11(families_from_db, individuals_from_db)
# Sprint 3
usrun.us12(families_from_db, individuals_from_db)
usrun.us19(families_from_db, individuals_from_db)
# Sprint 4
usrun.us34(families_from_db, individuals_from_db)
usrun.us36(families_from_db, individuals_from_db)
# Logger Print
usrun.logger.print_log()
