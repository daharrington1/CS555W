from tabulate import tabulate
import string
# Used only for data mocking
import random


# Concrete data can be either dictionaries or concrete classes. As long as the data required in these are
# provided in some form the code can easily be adapted

# Placeholder individual
class IndividualPlaceholder:
    id = ""
    name = ""
    sex = ""
    birt = ""
    age = 0
    deat = ""
    fams = ""
    famc = ""

    def __init__(self, id, name, sex, birt, age, deat, fams, famc):
        self.id = id
        self.name = name
        self.sex = sex
        self.birt = birt
        self.age = age
        self.deat = deat
        self.fams = fams
        self.famc = famc


# Placeholder Family object
class FamilyPlaceholder:
    id = ""
    married = ""
    divorced = False
    husband_id = ""
    husband_name = ""
    wife_id = ""
    wife_name = ""
    children = []

    def __init__(self, id, married, divorced, husband_id, husband_name, wife_id, wife_name, children):
        self.id = id
        self.married = married
        self.divorced = divorced
        self.husband_id = husband_id
        self.husband_name = husband_name
        self.wife_id = wife_id
        self.wife_name = wife_name
        self.children = children


class TablePrinter:
    """
    Static class which contains the logic to print out individuals or families into a formatted table
    """

    # String defines, minus for headers
    _table_format_type = "pretty"
    _table_label_individual = "Individuals"
    _table_label_family = "Families"

    @classmethod
    def print_individuals(cls, individuals):
        """
        Prints the provided list/tuple of individuals as a table.
        An individual is an object which has these fields:
        - id -- Expected String
        - name -- Expected String
        - sex -- Expected char of 'M' or 'F'
        - birt -- String of a date in form "MM DD YYYY"
        - age -- Non-negative Integer
        - deat -- String of death date, in form "MM DD YYYY" if it exists, None if they are alive
        - famc -- The family id of where they are a child, None if they are not a child
        - fams -- The family id of where they are a spouse, None if they are unmarried
        :param individuals: A list / tuple of individuals. No-ops on none or empty input
        :return: None
        """

        # Map 1:1, except
        # - Set isAlive based on the logical not of the individual's death date
        # - Deat, famc, and fams are replaced with "N/a" if not present, or taken literally if they are
        headers = ["Id", "Name", "Gender", "Birthday", " Age", "Alive", "Death", "Child", "Spouse"]
        mapper = lambda individual: (individual.id, individual.name, individual.sex, individual.birt, individual.age,
                                     False if individual.deat is not None else True,
                                     individual.deat if individual.deat is not None else "N/a",
                                     individual.famc if individual.famc is not None else "N/a",
                                     individual.fams if individual.fams is not None else "N/a")

        cls._print_sorted_mapped_table(cls._table_label_individual, individuals, headers, mapper)

    @classmethod
    def print_families(cls, families):
        """
         Prints the provided list/tuple of familes as a table.
         A family is defined as having these fields:
         - id -- String, The id of the family
         - married --  String, a date of format "MM DD YYYY"
         - divorced -- boolean
         - husbandId -- String, The id of individual which is the husband
         - husbandName -- String, the name of the individual with husbandID
         - wifeId -- String, The id of individual which is the wife
         - wifeName -- String, the name of the individual with wifeID
         - Children -- List, if no children then None
        :param families: The list/tuple to print. If None or empty, the function no-ops
        :return: None
        """
        headers = ["Id", "Married", "Divorced", "Husband Id", "Husband Name", "Wife Id", "Wife Name", "Children"]
        # Map 1:1, except replace divorced with "N/a" if there was no divorce
        # If children is None or size 0, map to string "None", otherwise sorted in ascending order
        mapper = lambda fam: (fam.id, fam.married, fam.divorced if fam.divorced else "N/a", fam.husband_id,
                              fam.husband_name, fam.wife_id, fam.wife_name,
                              sorted(fam.children) if fam.children is not None and len(fam.children) > 0 else "None")

        cls._print_sorted_mapped_table(cls._table_label_family, families, headers, mapper)

    @classmethod
    def _print_sorted_mapped_table(cls, printed_label, data, headers, data_map_lambda):
        """
        Prints the formatted table with ids in ascending order
        Sorts the data based off the 0th index
        :param printed_label: The label to print above the table.
        :param data: The raw data which to be processed by the data_map_lambda
        :param headers: The headers to display at the top
        :param data_map_lambda: The mapping lambda to process the data. 0th index of resulting map will be the sort key
        :return:
        """
        if data is None or type(data) is not list and type(data) is not tuple:
            return

        print(printed_label)
        mapped_data = sorted(list(map(data_map_lambda, data)), key=lambda it: it[0])
        print(tabulate(mapped_data, headers, cls._table_format_type))


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
            generated.append(IndividualPlaceholder(generated_id, name, gender, birth, random.randint(18, 100),
                                                   cls._generate_date(), cls._generate_id_or_none(),
                                                   cls._generate_id_or_none()))
        return generated

    @classmethod
    def generate_test_families(cls, amount):
        random.seed()
        generated = []
        for x in range(amount):
            children = list(cls._generate_id() for i in range(random.randint(0, 3)))
            generated.append(FamilyPlaceholder(cls._generate_id(), cls._generate_date(), cls._generateDateOrNone(),
                                               cls._generate_id(), cls._generate_full_name(), cls._generate_id(),
                                               cls._generate_full_name(), children))
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
