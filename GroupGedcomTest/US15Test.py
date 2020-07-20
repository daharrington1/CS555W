import unittest
from Utils.UserStory15 import us15_sibling_count
from Utils.Utils import normalize_family_entry


#
# Test Scripts for User Story 15: Get all siblings greater than a given count
# Per Customer (i.e. Prof Rowland) - only need to look at immediate families
# and not half families.
# Author: Debbie Harrington
#
# Test Scripts for verifying US15 user story
#

class US15Test(unittest.TestCase):
    families = None
    individuals = None
    famMap = None
    indMap = None

    def setUp(self):
        self.families = []
        self.individuals = []
        self.famMap = {}
        self.indMap = {}
        self.seed_data()

    def tearDown(self):
        self.families = None
        self.individuals = None
        self.famMap = None
        self.indMap = None

    def seed_data(self):
        # seed initial testing data
        self.families.append({
            "HUSB": ["I1"],
            "WIFE": ["I2"],
            "CHIL": ["I10"],
            "MARR": [1, 1, 2009],
            "NOTE": "JAY/GLORIA FAMILY",
            "FAM": "F1"
         })
        self.families.append({
            "HUSB": ["I1"],
            "WIFE": ["I3"],
            "CHIL": ["I4", "I6"],
            "MARR": [1, 2, 1968],
            "DIV": [1, 2, 2003],
            "NOTE": "JAY/DEEDEE",
            "FAM": "F2"
         })
        self.families.append({
            "HUSB": ["I8"],
            "WIFE": ["I2"],
            "CHIL": ["I9"],
            "MARR": [1, 1, 1995],
            "DIV": [1, 1, 2006],
            "NOTE": "JAVIER/GLORIA",
            "FAM": "F3"
         })
        self.families.append({
            "HUSB": ["I4", "I5"],
            "CHIL": ["I14", "I15", "I4", "I5"],
            "MARR": [1, 1, 2014],
            "NOTE": "PRITCHETT/TUCKER FAMILY",
            "FAM": "F4",
            "WIFE": "-"
         })
        self.families.append({
            "HUSB": ["I16"],
            "WIFE": ["I17"],
            "CHIL": ["I5", "I15"],
            "MARR": [1, 1, 1963],
            "NOTE": "MERLE/BARB FAMILY",
            "FAM": "F5"
         })
        self.families.append({
            "HUSB": ["I7"],
            "WIFE": ["I6"],
            "CHIL": ["I20", "I24", "I25"],
            "MARR": [1, 4, 1993],
            "NOTE": "PHIL/CLAIRE FAMILY",
            "FAM": "F6"
         })
        self.families.append({
            "HUSB": ["I11"],
            "WIFE": ["I13"],
            "CHIL": ["I7"],
            "MARR": [1, 1, 1965],
            "NOTE": "FRANK/GRACE FAMILY",
            "FAM": "F7"
         })
        self.families.append({
            "HUSB": ["I11"],
            "WIFE": ["I12"],
            "MARR": [5, 4, 2017],
            "NOTE": "FRANK/LORRAINE FAMILY ",
            "FAM": "F8"
         })
        self.families.append({
            "WIFE": ["I15"],
            "CHIL": ["I19"],
            "NOTE": "PAMERON TUCKER FAMILY",
            "FAM": "F9",
            "MARR": "-",
            "HUSB": "-"
         })
        self.families.append({
            "HUSB": ["I21"],
            "WIFE": ["I20"],
            "CHIL": ["I22", "I23"],
            "MARR": [8, 3, 2019],
            "FAM": "F10",
            "NOTE": "MARSHALL/DUNPHY FAMILY"
         })
        self.families.append({
            "HUSB": ["I26"],
            "WIFE": ["I27"],
            "CHIL": ["I26"],
            "MARR": [16, 1, 2015],
            "NOTE": "MarryToChildFAMILY",
            "FAM": "F11"
         })
        self.individuals.append({
            "NAME": "Jay/Pritchett/",
            "SEX": "M",
            "BIRT": [28, 12, 2021],
            "FAMS": ["F1", "F2"],
            "AGE": -1,
            "INDI": "I1"
         })
        self.individuals.append({
            "NAME": "Gloria/Unknown/",
            "SEX": "F",
            "BIRT": [10, 5, 1971],
            "FAMS": ["F1", "F3"],
            "AGE": 49,
            "INDI": "I2"
         })
        self.individuals.append({
            "NAME": "DeDe/Pritchett/",
            "SEX": "F",
            "BIRT": [23, 1, 1947],
            "DEAT": [1, 10, 2100],
            "FAMS": ["F2"],
            "AGE": 153,
            "INDI": "I3"
         })
        self.individuals.append({
            "NAME": "Mitchell/Pritchett/",
            "SEX": "M",
            "BIRT": [1, 6, 1975],
            "FAMS": ["F4"],
            "FAMC": ["F2"],
            "AGE": 45,
            "INDI": "I4"
         })
        self.individuals.append({
            "NAME": "Cameron/Tucker/",
            "SEX": "M",
            "BIRT": [29, 2, 1972],
            "FAMS": ["F4"],
            "FAMC": ["F5"],
            "AGE": 48,
            "INDI": "I5"
         })
        self.individuals.append({
            "NAME": "Claire/Pritchett/",
            "SEX": "F",
            "BIRT": [3, 3, 1970],
            "FAMS": ["F6"],
            "FAMC": ["F2"],
            "AGE": 50,
            "INDI": "I6"
         })
        self.individuals.append({
            "NAME": "Phil/Dunphy/",
            "SEX": "M",
            "BIRT": [3, 4, 1967],
            "FAMS": ["F6"],
            "FAMC": ["F7"],
            "AGE": 53,
            "INDI": "I7"
         })
        self.individuals.append({
            "NAME": "Javier/Delgado/",
            "SEX": "M",
            "BIRT": [1, 1, 1969],
            "FAMS": ["F3"],
            "AGE": 51,
            "INDI": "I8"
         })
        self.individuals.append({
            "NAME": "Manny/Delgado/",
            "SEX": "M",
            "BIRT": [4, 1, 1999],
            "FAMC": ["F3"],
            "AGE": 21,
            "INDI": "I9"
         })
        self.individuals.append({
            "NAME": "Joe/Pritchett/",
            "SEX": "M",
            "BIRT": [4, 1, 2013],
            "FAMC": ["F1"],
            "NOTE": "Duplicatenameandbirthdayindividual",
            "AGE": 7,
            "INDI": "I10"
         })
        self.individuals.append({
            "NAME": "Jay/Pritchett/",
            "SEX": "M",
            "BIRT": [28, 12, 2021],
            "AGE": -1,
            "INDI": "I89"
         })
        self.individuals.append({
            "NAME": "Frank/Dunphy/",
            "SEX": "M",
            "BIRT": [1, 1, 1945],
            "DEAT": [15, 1, 2020],
            "FAMS": ["F7", "F8"],
            "AGE": 75,
            "INDI": "I11"
         })
        self.individuals.append({
            "NAME": "Lorraine/Dunphy/",
            "SEX": "F",
            "BIRT": [1, 1, 1965],
            "FAMS": ["F8"],
            "AGE": 55,
            "INDI": "I12"
         })
        self.individuals.append({
            "NAME": "Grace/Dunphy/",
            "SEX": "F",
            "BIRT": [1, 1, 1945],
            "DEAT": [1, 1, 2009],
            "FAMS": ["F7"],
            "AGE": 64,
            "INDI": "I13"
         })
        self.individuals.append({
            "NAME": "Lily/Tucker-Pritchett/",
            "SEX": "F",
            "BIRT": [19, 2, 2008],
            "FAMC": ["F4"],
            "AGE": 12,
            "INDI": "I14"
         })
        self.individuals.append({
            "NAME": "Rexford/Tucker-Pritchett/",
            "SEX": "M",
            "BIRT": [1, 4, 2020],
            "FAMC": ["F4"],
            "AGE": 0,
            "INDI": "I15"
         })
        self.individuals.append({
            "NAME": "Merle/Tucker/",
            "SEX": "M",
            "BIRT": [1, 1, 1943],
            "FAMS": ["F5"],
            "AGE": 77,
            "INDI": "I16"
         })
        self.individuals.append({
            "NAME": "Barb/Tucker/",
            "SEX": "F",
            "BIRT": [1, 1, 1943],
            "FAMS": ["F5"],
            "AGE": 77,
            "INDI": "I17"
         })
        self.individuals.append({
            "NAME": "Pameron/Tucker/",
            "SEX": "F",
            "BIRT": [1, 1, 1970],
            "FAMS": ["F9"],
            "FAMC": ["F5"],
            "AGE": 50,
            "INDI": "I15"
         })
        self.individuals.append({
            "NAME": "Calhoun/Tucker/",
            "SEX": "M",
            "BIRT": [5, 4, 2017],
            "FAMC": ["F9"],
            "AGE": 3,
            "INDI": "I19"
         })
        self.individuals.append({
            "NAME": "Haley/Dunphy/",
            "SEX": "F",
            "BIRT": [10, 12, 1993],
            "FAMS": ["F10"],
            "FAMC": ["F6"],
            "AGE": 27,
            "INDI": "I20"
         })
        self.individuals.append({
            "NAME": "Dylan/Marshall/",
            "SEX": "M",
            "BIRT": [3, 4, 1991],
            "FAMS": ["F10"],
            "AGE": 29,
            "INDI": "I21"
         })
        self.individuals.append({
            "NAME": "Poppy/Marshall/",
            "SEX": "F",
            "BIRT": [8, 5, 2019],
            "FAMC": ["F10"],
            "AGE": 1,
            "INDI": "I22"
         })
        self.individuals.append({
            "NAME": "George/Hastings/",
            "SEX": "M",
            "BIRT": [8, 5, 2019],
            "FAMC": ["F10"],
            "AGE": 1,
            "INDI": "I23"
         })
        self.individuals.append({
            "NAME": "Alex/Dunphy/",
            "SEX": "F",
            "BIRT": [14, 1, 1997],
            "FAMC": ["F6"],
            "AGE": 23,
            "INDI": "I24"
         })
        self.individuals.append({
            "NAME": "Luke/Dunphy/",
            "SEX": "M",
            "BIRT": [28, 11, 1998],
            "FAMC": ["F6"],
            "NOTE": "JAY/GLORIAFAMILY",
            "AGE": 22, "INDI": "I25"
         })
        self.individuals.append({
            "NAME": "Luke/Hastings/",
            "SEX": "M",
            "BIRT": [28, 11, 1998],
            "FAMS": ["F11"],
            "FAMC": ["F11"],
            "NOTE": "MarryToChildFAMILY",
            "AGE": 22,
            "INDI": "I26"
         })
        self.individuals.append({
            "NAME": "Mary/Hastings/",
            "SEX": "F",
            "BIRT": [28, 11, 1970],
            "FAMS": ["F11"],
            "NOTE": "MarryToChildFAMILY",
            "AGE": 50,
            "INDI": "I27"
         })

        for ind in self.individuals:
            self.indMap[ind["INDI"]] = ind

        for fam in self.families:
            self.famMap[fam["FAM"]] = normalize_family_entry(fam)

    def test_US15_noinputs(self):
        # bad inputs
        with self.assertRaises(Exception):
            us15_sibling_count(None, None)

        with self.assertRaises(Exception):
            us15_sibling_count(self.indMap)

    def test_US15_DefaultCount(self):
        # should return 10 families with siblings
        ret = us15_sibling_count(self.famMap)
        self.assertEqual(len(ret), 10,
                         "Did not get the expected results")

    def test_US15_DefaultOneText(self):
        # should get the following families with siblings
        expected_ret = [('F1', ['I10']),
                        ('F2', ['I4', 'I6']),
                        ('F3', ['I9']),
                        ('F4', ['I14', 'I15', 'I4', 'I5']),
                        ('F5', ['I15', 'I5']),
                        ('F6', ['I20', 'I24', 'I25']),
                        ('F7', ['I7']),
                        ('F9', ['I19']),
                        ('F10', ['I22', 'I23']),
                        ('F11', ['I26'])]
        ret = us15_sibling_count(self.famMap)
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")
        self.assertEqual(len(ret[0][1]), 1,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[1][1]), 2,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[2][1]), 1,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[3][1]), 4,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[4][1]), 2,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[5][1]), 3,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[6][1]), 1,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[7][1]), 1,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[8][1]), 2,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[9][1]), 1,
                         "Did not match entry 1 length")

    def test_US15_TwoOrMore(self):
        # should get 5 families with 2 or more siblings
        ret = us15_sibling_count(self.famMap, 2)
        self.assertEqual(len(ret), 5,
                         "Did not get the expected results")

    def test_US15_TwoOrMoreText(self):
        # should get 5 families with 2 or more siblings
        expected_ret = [('F2', ['I4', 'I6']),
                        ('F4', ['I14', 'I15', 'I4', 'I5']),
                        ('F5', ['I15', 'I5']),
                        ('F6', ['I20', 'I24', 'I25']),
                        ('F10', ['I22', 'I23'])]
        ret = us15_sibling_count(self.famMap, 2)
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")
        self.assertEqual(len(ret[0][1]), 2,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[1][1]), 4,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[2][1]), 2,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[3][1]), 3,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[4][1]), 2,
                         "Did not match entry 1 length")

    def test_US15_ThreeOrMore(self):
        # should get 2 families with 3 or more siblings
        ret = us15_sibling_count(self.famMap, 3)
        self.assertEqual(len(ret), 2,
                         "Did not get the expected results")

    def test_US15_ThreeOrMoreText(self):
        # should get 2 families with 3 or more siblings
        expected_ret = [('F4', ['I14', 'I15', 'I4', 'I5']),
                        ('F6', ['I20', 'I24', 'I25'])]
        ret = us15_sibling_count(self.famMap, 3)
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")
        self.assertEqual(len(ret[0][1]), 4,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[1][1]), 3,
                         "Did not match entry 1 length")

    def test_US15_FourOrMore(self):
        # should get 1 family with 4 or more siblings
        ret = us15_sibling_count(self.famMap, 4)
        self.assertEqual(len(ret), 1,
                         "Did not get the expected results")

    def test_US15_FourOrMoreText(self):
        # should get 1 family with 4 or more siblings
        expected_ret = [('F4', ['I14', 'I15', 'I4', 'I5'])]
        ret = us15_sibling_count(self.famMap, 4)
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")
        self.assertEqual(len(ret[0][1]), 4,
                         "Did not match entry 1 length")

    def test_US15_FiveOrMore(self):
        # should get zero family with 5 or more siblings
        ret = us15_sibling_count(self.famMap, 5)
        self.assertEqual(len(ret), 0,
                         "Did not get the expected results")

    def test_US15_FiveOrMoreText(self):
        # should get zero family with 5 or more siblings
        expected_ret = []
        ret = us15_sibling_count(self.famMap, 5)
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

    def test_US15_FifteenorMore(self):
        # add in siblings to family 4 to make 15 - should get one family to match
        for i in range(28, 39):
            self.indMap["I"+str(i)] = {
                "NAME": "I" + str(i) + "/Hastings/",
                "SEX": "F",
                "BIRT": [28, 11, 1970],
                "FAMC": ["F4"],
                "NOTE": "Adding Child to Family F4",
                "INDI": "I" + str(i)
            }
            self.famMap["F4"]["CHIL"].append("I" + str(i))

        ret = us15_sibling_count(self.famMap, 15)
        self.assertEqual(len(ret), 1,
                         "Did not get the expected results")

    def test_US15_FifteenorMoreText(self):
        # add in siblings to family 4 to make 15 - should get one family to match
        for i in range(28, 39):
            self.indMap["I"+str(i)] = {
                "NAME": "I" + str(i) + "/Hastings/",
                "SEX": "F",
                "BIRT": [28, 11, 1970],
                "FAMC": ["F4"],
                "NOTE": "Adding Child to Family F4",
                "INDI": "I" + str(i)
            }
            self.famMap["F4"]["CHIL"].append("I" + str(i))

        expected_ret = [('F4', ['I14', 'I15', 'I28', 'I29', 'I30', 'I31', 'I32', 'I33', 'I34',
                         'I35', 'I36', 'I37', 'I38', 'I4', 'I5'])]
        ret = us15_sibling_count(self.famMap, 15)
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")
        self.assertEqual(len(ret[0][1]), 15,
                         "Did not match entry 1 length")

    def test_US15_SixteenorMore(self):
        # add in siblings to family 4 to make 15 - should get one family to match 15 or greater
        for i in range(28, 40):
            self.indMap["I"+str(i)] = {
                "NAME": "I" + str(i) + "/Hastings/",
                "SEX": "F",
                "BIRT": [28, 11, 1970],
                "FAMC": ["F4"],
                "NOTE": "Adding Child to Family F4",
                "INDI": "I" + str(i)
            }
            self.famMap["F4"]["CHIL"].append("I" + str(i))

        expected_ret = [('F4', ['I14', 'I15', 'I28', 'I29', 'I30', 'I31', 'I32', 'I33', 'I34',
                         'I35', 'I36', 'I37', 'I38', 'I39', 'I4', 'I5'])]
        ret = us15_sibling_count(self.famMap, 15)
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")
        self.assertEqual(len(ret), 1,
                         "Did not match entry 1 length")
        self.assertEqual(len(ret[0][1]), 16,
                         "Did not match entry 1 length")

    def test_US15_FourteenorMore(self):
        # add in siblings to family 4 to make 14 - should get zero family to match 15 or greater
        for i in range(28, 38):
            self.indMap["I"+str(i)] = {
                "NAME": "I" + str(i) + "/Hastings/",
                "SEX": "F",
                "BIRT": [28, 11, 1970],
                "FAMC": ["F4"],
                "NOTE": "Adding Child to Family F4",
                "INDI": "I" + str(i)
            }
            self.famMap["F4"]["CHIL"].append("I" + str(i))

        expected_ret = []
        ret = us15_sibling_count(self.famMap, 15)
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")
        self.assertEqual(len(ret), 0,
                         "Did not match entry 1 length")


if __name__ == '__main__':
    unittest.main()
