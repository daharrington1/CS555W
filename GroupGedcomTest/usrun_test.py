import unittest
from usrun import IDtoINDI, IDinFam, months, unique_families, first_cousin_not_marry,\
    upcoming_birthdays, no_bigamy_sev_fam, no_bigamy_one_fam, large_age_difference, recent_deaths,\
    parents_not_too_old
import copy


# Individuals and Families: Debbie Harrington
# User and Author : Chengyi Zhang
# Test Scripts for User Stories
#
# Test Scripts for verifying Chengyi Zhang sprints
#

class usruntest(unittest.TestCase):
    families = None
    individuals = None

    def setUp(self):
        self.seed_data()

    def tearDown(self):
        self.families = None
        self.individuals = None

    def seed_data(self):
        # seed family data - don't need individual data for this test suite

        self.families = []
        self.families.append(
            {"HUSB": ["I1"], "WIFE": ["I2"], "CHIL": ["I10"], "MARR": [1, 1, 2009], "NOTE": "JAY/GLORIA FAMILY",
             "FAM": "F1"})
        self.families.append(
            {"HUSB": ["I1"], "WIFE": ["I3"], "CHIL": ["I4", "I6"], "MARR": [1, 1, 2025], "DIV": [28, 6, 2020],
             "NOTE": "JAY/DEEDEE", "FAM": "F2"})
        self.families.append({"HUSB": ["I8"], "WIFE": ["I2"], "CHIL": ["I9"], "MARR": [1, 1, 1995], "DIV": [1, 1, 2006],
                              "NOTE": "JAVIER/GLORIA", "FAM": "F3"})
        self.families.append(
            {"HUSB": ["I4", "I5"], "CHIL": ["I14", "I15"], "MARR": [1, 1, 2014], "NOTE": "PRITCHETT/TUCKER FAMILY",
             "FAM": "F4", "WIFE": "-"})
        self.families.append(
            {"HUSB": ["I16"], "WIFE": ["I17"], "CHIL": ["I5", "I18"], "MARR": [1, 1, 1963], "NOTE": "MERLE/BARB FAMILY",
             "FAM": "F5"})
        self.families.append({"HUSB": ["I7"], "WIFE": ["I6"], "CHIL": ["I20", "I24", "I25"], "MARR": [1, 4, 1993],
                              "NOTE": "PHIL/CLAIRE FAMILY", "FAM": "F6"})
        self.families.append(
            {"HUSB": ["I11"], "WIFE": ["I13"], "CHIL": ["I7"], "MARR": [1, 1, 1965], "NOTE": "FRANK/GRACE FAMILY",
             "FAM": "F7"})
        self.families.append(
            {"HUSB": ["I11"], "WIFE": ["I12"], "MARR": [5, 4, 2017], "NOTE": "FRANK/LORRAINE FAMILY ", "FAM": "F8"})
        self.families.append(
            {"WIFE": ["I18"], "CHIL": ["I19"], "NOTE": "PAMERON TUCKER FAMILY", "FAM": "F9", "MARR": "-", "HUSB": "-"})
        self.families.append(
            {"HUSB": ["I21"], "WIFE": ["I20"], "CHIL": ["I22", "I23"], "MARR": [8, 3, 2019], "FAM": "F10",
             "NOTE": "MARSHALL/DUNPHY FAMILY"})
        self.families.append(
            {"HUSB": ["I26"], "WIFE": ["I27"], "CHIL": ["I26"], "MARR": [16, 1, 2018], "NOTE": "MarryToChildFAMILY",
             "FAM": "F11"})

        self.individuals = []
        self.individuals.append(
            {"NAME": "Jay/Pritchett/", "SEX": "M", "BIRT": [28, 12, 2021], "FAMS": ["F1", "F2"], "AGE": -1,
             "INDI": "I1"})
        self.individuals.append(
            {"NAME": "Gloria/Unknown/", "SEX": "F", "BIRT": [10, 5, 1971], "FAMS": ["F1", "F3"], "AGE": 49,
             "INDI": "I2"})
        self.individuals.append(
            {"NAME": "DeDe/Pritchett/", "SEX": "F", "BIRT": [23, 1, 1947], "DEAT": [1, 10, 2100], "FAMS": ["F2"],
             "AGE": 73, "INDI": "I3"})
        self.individuals.append(
            {"NAME": "Mitchell/Pritchett/", "SEX": "M", "BIRT": [1, 6, 1975], "FAMS": ["F4"], "FAMC": ["F2"], "AGE": 45,
             "INDI": "I4"})
        self.individuals.append(
            {"NAME": "Cameron/Tucker/", "SEX": "M", "BIRT": [29, 2, 1972], "FAMS": ["F4"], "FAMC": ["F5"], "AGE": 48,
             "INDI": "I5"})
        self.individuals.append(
            {"NAME": "Claire/Pritchett/", "SEX": "F", "BIRT": [3, 3, 1970], "FAMS": ["F6"], "FAMC": ["F2"], "AGE": 50,
             "INDI": "I6"})
        self.individuals.append(
            {"NAME": "Phil/Dunphy/", "SEX": "M", "BIRT": [3, 4, 1967], "FAMS": ["F6"], "FAMC": ["F7"], "AGE": 53,
             "INDI": "I7"})
        self.individuals.append(
            {"NAME": "Javier/Delgado/", "SEX": "M", "BIRT": [1, 1, 1969], "FAMS": ["F3"], "AGE": 51, "INDI": "I8"})
        self.individuals.append(
            {"NAME": "Manny/Delgado/", "SEX": "M", "BIRT": [4, 1, 1999], "FAMC": ["F3"], "AGE": 21, "INDI": "I9"})
        self.individuals.append({"NAME": "Joe/Pritchett/", "SEX": "M", "BIRT": [4, 1, 2013], "FAMC": ["F1"],
                                 "NOTE": "Duplicatenameandbirthdayindividual", "AGE": 7, "INDI": "I10"})
        self.individuals.append(
            {"NAME": "Jay/Pritchett/", "SEX": "M", "BIRT": [28, 12, 2021], "AGE": -1, "INDI": "I89"})
        self.individuals.append(
            {"NAME": "Frank/Dunphy/", "SEX": "M", "BIRT": [1, 1, 1945], "DEAT": [15, 1, 2020], "FAMS": ["F7", "F8"],
             "AGE": 75, "INDI": "I11"})
        self.individuals.append(
            {"NAME": "Lorraine/Dunphy/", "SEX": "F", "BIRT": [1, 1, 1965], "FAMS": ["F8"], "AGE": 55, "INDI": "I12"})
        self.individuals.append(
            {"NAME": "Grace/Dunphy/", "SEX": "F", "BIRT": [1, 1, 1945], "DEAT": [1, 1, 2009], "FAMS": ["F7"], "AGE": 64,
             "INDI": "I13"})
        self.individuals.append(
            {"NAME": "Lily/Tucker-Pritchett/", "SEX": "F", "BIRT": [19, 2, 2008], "FAMC": ["F4"], "AGE": 12,
             "INDI": "I14"})
        self.individuals.append(
            {"NAME": "Rexford/Tucker-Pritchett/", "SEX": "M", "BIRT": [1, 4, 2020], "FAMC": ["F4"], "AGE": 0,
             "INDI": "I15"})
        self.individuals.append(
            {"NAME": "Merle/Tucker/", "SEX": "M", "BIRT": [1, 1, 1943], "FAMS": ["F5"], "AGE": 77, "INDI": "I16"})
        self.individuals.append(
            {"NAME": "Barb/Tucker/", "SEX": "F", "BIRT": [1, 1, 1943], "FAMS": ["F5"], "AGE": 77, "INDI": "I17"})
        self.individuals.append(
            {"NAME": "Pameron/Tucker/", "SEX": "F", "BIRT": [1, 1, 1970], "FAMS": ["F9"], "FAMC": ["F5"], "AGE": 50,
             "INDI": "I18"})
        self.individuals.append(
            {"NAME": "Calhoun/Tucker/", "SEX": "M", "BIRT": [5, 4, 2017], "FAMC": ["F9"], "AGE": 3, "INDI": "I19"})
        self.individuals.append(
            {"NAME": "Haley/Dunphy/", "SEX": "F", "BIRT": [10, 12, 1993], "FAMS": ["F10"], "FAMC": ["F6"], "AGE": 27,
             "INDI": "I20"})
        self.individuals.append(
            {"NAME": "Dylan/Marshall/", "SEX": "M", "BIRT": [3, 4, 1991], "FAMS": ["F10"], "AGE": 29, "INDI": "I21"})
        self.individuals.append(
            {"NAME": "Poppy/Marshall/", "SEX": "F", "BIRT": [8, 5, 2019], "FAMC": ["F10"], "AGE": 1, "INDI": "I22"})
        self.individuals.append(
            {"NAME": "George/Hastings/", "SEX": "M", "BIRT": [8, 5, 2019], "FAMC": ["F10"], "AGE": 1, "INDI": "I23"})
        self.individuals.append(
            {"NAME": "Alex/Dunphy/", "SEX": "F", "BIRT": [14, 1, 1997], "FAMC": ["F6"], "AGE": 23, "INDI": "I24"})
        self.individuals.append(
            {"NAME": "Luke/Dunphy/", "SEX": "M", "BIRT": [28, 11, 1998], "FAMC": ["F6"], "NOTE": "JAY/GLORIAFAMILY",
             "AGE": 22, "INDI": "I25"})
        self.individuals.append(
            {"NAME": "Luke/Hastings/", "SEX": "M", "BIRT": [28, 11, 1998], "FAMS": ["F11"], "FAMC": ["F11"],
             "NOTE": "MarryToChildFAMILY", "AGE": 22, "INDI": "I26"})
        self.individuals.append({"NAME": "Mary/Hastings/", "SEX": "F", "BIRT": [28, 11, 1970], "FAMS": ["F11"],
                                 "NOTE": "MarryToChildFAMILY", "AGE": 50, "INDI": "I27"})

    # Test Tools

    def test_iti(self):
        # test IDtoINDI()
        self.assertEqual(len(IDtoINDI(self.individuals)), 28)
        self.assertEqual(IDtoINDI(self.individuals)['I1'], self.individuals[0])

    def test_mo(self):
        # test months
        self.assertEqual(months[1], 'JAN')
        self.assertNotEqual(months[6], 'JUL')

    def test_iif(self):
        # test IDinFam()
        self.assertEqual(len(IDinFam(self.families)), 18)
        self.assertEqual(IDinFam(self.families)['I1'], [self.families[0], self.families[1]])

    # Test US24

    def test_uf(self):
        # test unique_families()
        tmpfam = self.families.copy()
        tmpfam.append(
            {"HUSB": ["I1"], "WIFE": ["I2"], "CHIL": ["I10"], "MARR": [1, 1, 2009], "NOTE": "JAY/GLORIA FAMILY",
             "FAM": "F12"})
        self.assertEqual(unique_families(tmpfam, self.individuals), [('1/1/2009', 'F1', 'F12')])
        self.assertEqual(unique_families(self.families, self.individuals), [])
        tmpfam.append(
            {"HUSB": ["I1"], "WIFE": ["I2"], "CHIL": ["I10"], "MARR": [1, 1, 2009], "NOTE": "JAY/GLORIA FAMILY",
             "FAM": "F12"})
        self.assertEqual(unique_families(tmpfam, self.individuals),
                         [('1/1/2009', 'F1', 'F12'), ('1/1/2009', 'F1', 'F12'), ('1/1/2009', 'F12', 'F12')])

    # Test US38

    def test_ub(self):
        # test upcoming_birthdays()
        tmpind = self.individuals.copy()
        tmpind.append({"NAME": "Luke/Hastings/", "SEX": "M", "BIRT": [29, 8, 1998], "FAMS": ["F11"], "FAMC": ["F11"],
                       "NOTE": "MarryToChildFAMILY", "AGE": 22, "INDI": "I30"})
        self.assertEqual(upcoming_birthdays(tmpind), [("I30", "AUG 29")])

    # Test US11

    def test_nb1(self):
        # test no_bigamy_one_fam
        tmpfam = copy.deepcopy(self.families)
        self.assertEqual(len(no_bigamy_one_fam(self.families, self.individuals)), 0)
        tmpfam[0]['WIFE'].append('I3')
        self.assertEqual(no_bigamy_one_fam(tmpfam, self.individuals), ['F1'])

    def test_nbs(self):
        # test no_bigamy_sev_fam
        tmpfam = self.families.copy()
        self.assertEqual(no_bigamy_sev_fam(self.families, self.individuals), ['I1'])
        tmpfam.append({"HUSB": "-", "WIFE": ["I2", 'I3'], "CHIL": ["I10"], "MARR": [1, 1, 2009], "FAM": "F20"})
        self.assertEqual(no_bigamy_sev_fam(tmpfam, self.individuals), ['I1', 'I2'])

    # Test US12

    def test_pnto(self):
        # test parents_not_too_old
        tmpfam = copy.deepcopy(self.families)
        self.assertEqual(len(parents_not_too_old(tmpfam, self.individuals)), 0)
        tmpfam[1]['CHIL'].append('I89')
        self.assertEqual(parents_not_too_old(tmpfam, self.individuals)[0][2], 'I3')

    # Test US19

    def test_fcsnm(self):
        # test first_cousin_not_marry
        tmpfam = copy.deepcopy(self.families)
        self.assertEqual(len(first_cousin_not_marry(tmpfam, self.individuals)), 0)
        tmpfam.append(
            {"HUSB": ["I16"], "WIFE": ["I6"], "CHIL": ['I10'], "MARR": [1, 1, 1963], "NOTE": "Test",
             "FAM": "F77"})
        tmpfam.append(
            {"HUSB": ["I14"], "WIFE": ["I10"], "MARR": [8, 3, 2019], "FAM": "F66",
             "NOTE": "Test"})
        self.assertEqual(len(first_cousin_not_marry(tmpfam, self.individuals)), 1)
        tmpfam.append(
            {"HUSB": ["I15"], "WIFE": ["I10"], "MARR": [8, 3, 2019], "FAM": "F55",
             "NOTE": "Test"})
        self.assertEqual(len(first_cousin_not_marry(tmpfam, self.individuals)), 2)

    # Test US34

    def test_lad(self):
        # test large_age_difference
        tmpfam = copy.deepcopy(self.families)
        tmpind = copy.deepcopy(self.individuals)
        self.assertEqual(len(large_age_difference(tmpfam, self.individuals)), 3)
        tmpind[0]['BIRT'][2] = 1975
        tmpind[0]['AGE'] = 45
        self.assertEqual(len(large_age_difference(tmpfam, tmpind)), 1)

    # Test US36

    def test_rd(self):
        # test recent_deaths
        tmpind = copy.deepcopy(self.individuals)
        self.assertEqual(len(recent_deaths(self.families, tmpind)), 0)
        tmpind.append(
            {"NAME": "Jay/Pritchett/", "SEX": "M", "BIRT": [28, 12, 2000],
             'DEAT': [20, 7, 2020], "FAMS": ["F1", "F2"], "AGE": -1,
             "INDI": "I333"}
        )
        self.assertEqual(len(recent_deaths(self.families, tmpind)), 1)


if __name__ == '__main__':
    unittest.main()
