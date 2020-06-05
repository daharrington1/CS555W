from tabulate import tabulate
import string
# Used only for data mocking
import random

"""
Class which contains the logic to print out individuals or families into a formatted table
"""
class TablePrinter:

    def __init__(self, individual_database):
        self.individual_database = individual_database

    individual_database = None

    # String defines, minus for headers
    _table_format_type = "pretty"
    _table_label_individual = "Individuals"
    _table_label_family = "Families"

    def print_individuals(self, individuals):
        """
    Prints the provided list/tuple of individuals as a table.
    An individual is a dictionary which has these fields:
    - INDI-- Expected String
    - NAME -- Expected String
    - SEX -- Expected char of 'M' or 'F'
    - BIRT -- String of a date in form ready to be displayed
    - AGE -- Non-negative Integer, will be replaced with a "-" if not in object
    - DEAT -- String of death date, in form ready to be displayed if it exists, None if they are alive
    - FAMC -- The family id of where they are a child, None if they are not a child
    - FAMS -- The family id of where they are a spouse, None if they are unmarried
    :param individuals: A list / tuple of individuals. No-ops on none or empty input
    :return: None
    """

        # Map 1:1, except
        # - Set isAlive based on the logical not of the individual's death date
        # - Deat, famc, and fams are replaced with "N/a" if not present, or taken literally if they are
        headers = ["Id", "Name", "Gender", "Birthday", " Age", "Alive", "Death", "Child", "Spouse"]
        mapper = lambda individual: (
            individual["INDI"],
            individual["NAME"],
            individual["SEX"],
            individual["BIRT"],
            individual["AGE"] if "AGE" in individual else "-",
            False if "DEAT" in individual else True,
            individual["DEAT"] if "DEAT" in individual else "N/a",
            individual["FAMC"] if "FAMC" in individual else "N/a",
            individual["FAMS"] if "FAMS" in individual else "N/a")

        self._print_sorted_mapped_table(self._table_label_individual, individuals, headers, mapper)

    """
     Prints the provided list/tuple of familes as a table.
     A family is defined as having these fields:
     - FAM -- String, The id of the family
     - MARR -- String, a date of format ready to be displayed
     - DIV -- String, date of format ready to be displayed, or None if no divorce
     - HUSB -- String, The id of individual which is the husband
     - WIFE -- String, The id of individual which is the wife
     - CHIL -- List, if no children then None
    :param families: The list/tuple to print. If None or empty, the function no-ops
    :return: None
    """
    def print_families(self, families):

        headers = ["Id", "Married", "Divorced", "Husband Id", "Husband Name", "Wife Id", "Wife Name", "Children"]
        # Map 1:1, except replace divorced with "N/a" if there was no divorce
        # If children is None or size 0, map to string "None", otherwise sorted in ascending order
        mapper = lambda fam: (fam["FAM"],
                              fam["MARR"],
                              fam["DIV"] if "DIV" in fam else "N/a",
                              fam["HUSB"],
                              self._look_up_name_by_id(fam["HUSB"]),
                              fam["WIFE"],
                              self._look_up_name_by_id(fam["WIFE"]),
                              sorted(fam["CHIL"]) if "Chil" in fam and len(fam["CHIL"]) > 0 else "None")

        self._print_sorted_mapped_table(self._table_label_family, families, headers, mapper)

    """
    Prints the formatted table with ids in ascending order
    Sorts the data based off the 0th index
    :param printed_label: The label to print above the table.
    :param data: The raw data which to be processed by the data_map_lambda
    :param headers: The headers to display at the top
    :param data_map_lambda: The mapping lambda to process the data. 0th index of resulting map will be the sort key
    :return:
    """
    def _print_sorted_mapped_table(self, printed_label, data, headers, data_map_lambda):
        if data is None or type(data) is not list and type(data) is not tuple:
            return

        print(printed_label)
        mapped_data = sorted(list(map(data_map_lambda, data)), key=lambda it: it[0])
        print(tabulate(mapped_data, headers, self._table_format_type))

    def _look_up_name_by_id(self, id,):
        if id is None or id == "ERR":
            return "ERR"
        # Remove the "@" as they are not in the user id
        return self.individual_database.getName(id[0].replace("@", "").strip())


class TestDataRunner:
    @classmethod
    # Generates noisy data to print. The data is *not* logically valid. Ie deaths before births etc
    def generate_test_users(cls, amount):
        random.seed()
        generated = []
        for x in range(amount):
            generated_id = cls._generate_id()
            name = cls._generate_full_name()
            gender = random.choice("M" + "F")
            birth = cls._generate_date()
            generated.append({
                'INDI': generated_id,
                'NAME': name,
                'SEX': gender,
                'BIRT': birth,
                'AGE': random.randint(18, 100),
                'DEAT': cls._generateDateOrNone(),
                'FAMC': cls._generateDateOrNone(),
                'FAMS': cls._generate_id()
            })

        return generated

    # WARNING: THIS WAS NOT UPDATED TO THE NEW DB LOOK UP, THIS *WILL* not give the correct value without being updated
    @classmethod
    def generate_test_families(cls, amount):
        random.seed()
        generated = []
        for x in range(amount):
            children = list(cls._generate_id() for i in range(random.randint(0, 3)))
            generated.append({
                'FAM': cls._generate_id(),
                'MARR': cls._generate_date(),
                'DIV': cls._generateDateOrNone(),
                'HUSB': cls._generate_id(),
                'HUSN': cls._generate_full_name(),
                'WIFE': cls._generate_id(),
                'WIFN': cls._generate_full_name(),
                'CHIL': children
            })

        return generated

    # Shared mocked data generators
    @classmethod
    def _generate_name(cls):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(random.randrange(3, 17)))

    @classmethod
    def _generate_full_name(cls):
        return cls._generate_name() + " " + cls._generate_name()

    @classmethod
    def _generate_id(cls):
        return random.randint(0, 5000)

    @classmethod
    def _generate_id_or_none(cls):
        # Chances are arbitrary to give noise to input
        return None if random.randint(0, 3) == 2 else cls._generate_id()

    @classmethod
    def _generate_date(cls):
        # MM DD YYYY, limited to 28 to pretend its a valid date for all months. Doesn't actually matter since
        # table performs no validation on printing
        return "{:02d} {:02d} {}".format(random.randint(1, 12), random.randint(1, 28), random.randint(1900, 2000))

    @classmethod
    def _generateDateOrNone(cls):
        # Chances are arbitrary to give noise to input
        return None if random.randint(0, 5) == 2 else cls._generate_date()

# Example run code
# TablePrinter.print_individuals(TestDataRunner.generate_test_users(5))
# TablePrinter.print_families(TestDataRunner.generate_test_families(5))
