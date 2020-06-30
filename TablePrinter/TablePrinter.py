from tabulate import tabulate

"""
Class which contains the logic to print out individuals or families into a formatted table
"""


class TablePrinter:

    def __init__(self, individual_database):
        self.individual_database = individual_database

    individual_database = None

    # String defines, minus for headers
    error_output = "-"
    _not_applicable = "N/A"
    _table_format_type = "pretty"
    table_label_dead_individual = "US29: Dead Individuals"
    _table_label_individual = "Individuals"
    _table_label_family = "Families"

    """
    Formats the provided list/tuple of individuals as a table.
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
    :param table_label: The label to put before the table. Empty string to suppress it. None uses default value
    :return: String of the formatted table
    """

    def format_individuals(self, individuals, table_label=None):
        table_label = table_label if type(table_label) is str else self._table_label_individual
        # Map 1:1, except
        # - Set isAlive based on the logical not of the individual's death date
        # - Deat, famc, and fams are replaced with self._not_applicable if not present, or taken literally if they are
        headers = ["Id", "Name", "Gender", "Birthday", " Age", "Alive", "Death", "Child Id", "Spouse Id"]

        return self._format_sorted_mapped_table(table_label, individuals,
                                                headers, self._individual_mapper)

    """
    Internal function to format an individual object from the database to a printable form
    """

    def _individual_mapper(self, individual):
        if "BIRT" not in individual:
            raise KeyError
        # 0 index grab on FAMC will always be a list of size one if it exist
        return (individual["INDI"],
                individual["NAME"],
                individual["SEX"],
                self.format_date(individual["BIRT"]),
                individual["AGE"] if "AGE" in individual else self.error_output,
                False if "DEAT" in individual else True,
                self.format_date(individual["DEAT"]) if "DEAT" in individual else self._not_applicable,
                individual["FAMC"][0] if "FAMC" in individual else self._not_applicable,
                ",".join(individual["FAMS"]) if "FAMS" in individual else self._not_applicable)

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
    :return: A string of the formatted table
    """

    def format_families(self, families):
        headers = ["Id", "Married", "Divorced", "Husband Id", "Husband Name", "Wife Id", "Wife Name", "Children Ids"]
        return self._format_sorted_mapped_table(self._table_label_family, families, headers, self._family_mapper)

    """
    Internal function to format a family object from the database to a printable form
    """

    def _family_mapper(self, fam):
        if "HUSB" not in fam or "WIFE" not in fam:
            raise KeyError

        # Map 1:1, except replace divorced with self._not_applicable if there was no divorce
        # If children is None or size 0, map to string "None", otherwise sorted in ascending order
        return (fam["FAM"],
                self.format_date(fam["MARR"]),
                self.format_date(fam["DIV"]) if "DIV" in fam else self._not_applicable,
                ",".join(fam["HUSB"]),
                self._look_up_name_by_id(fam["HUSB"]),
                ",".join(fam["WIFE"]),
                self._look_up_name_by_id(fam["WIFE"]),
                ",".join(sorted(fam["CHIL"])) if "CHIL" in fam and len(fam["CHIL"]) > 0 else "None")

    """
    Prints the formatted table with ids in ascending order
    Sorts the data based off the 0th index
    :param printed_label: The label to print above the table.
    :param data: The raw data which to be processed by the data_map_lambda
    :param headers: The headers to display at the top
    :param data_map_lambda: The mapping lambda to process the data. 0th index of resulting map will be the sort key
    :return: None
    """

    def _format_sorted_mapped_table(self, printed_label, data, headers, data_map_lambda):
        if data is None or type(data) is not list and type(data) is not tuple:
            return

        mapped_data = sorted(list(map(data_map_lambda, data)), key=lambda it: it[0])
        return "{}\n{}".format(printed_label, tabulate(mapped_data, headers, self._table_format_type))

    """
    Looks up all individual ids in the list, separated by ampersands
    :param individual_ids, the list of all ids to
    :return A string in the form "name0 & name1 & name2 ... & nameN" with no trailing " & "
    """

    def _look_up_name_by_id(self, individual_ids):
        if individual_ids is None or individual_ids == self.error_output:
            return self.error_output
        individual_ids = [individual_ids] if type(individual_ids) is not list else individual_ids
        all_names = []
        for individual in individual_ids:
            all_names.append(self.individual_database.getName(individual.replace("@", "").strip()))
        return " & ".join(all_names)

    """
    Converts a list date to a date for output
    :param A date as a list, with indexes [day, month, year]
    :return: String of the format in DD/MM/YYYY if valid format, otherwise strips [] from list toString
    """

    def format_date(self, date):
        if type(date) is not list or len(date) < 3:
            # Mal formed date, do not attempt to parse
            return self.error_output
        # DD MM YYYY.
        return "{:02d}/{:02d}/{:04d}".format(date[0], date[1], date[2])
