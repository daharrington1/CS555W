import unittest
from Utils.Logger import Logger
from Utils.spouseCrossChecker import spouseCrossChecker
from Utils.Utils import normalize_family_entry


#
# Test Scripts for User Story 14 & 32: Get all families with multiple births greater
# than a given count
# Author: Debbie Harrington/Chengyi Zhang
#
# Test Scripts for verifying US14 & US32 user stories
#

class US14_32Test(unittest.TestCase):
    families = None
    individuals = None
    famMap = None
    indMap = None
    logger = None
    spousecheck = None

    def setUp(self):
        self.families = []
        self.individuals = []
        self.famMap = {}
        self.indMap = {}
        self.logger = Logger()
        self.seed_data()
        self.spousecheck = None

    def tearDown(self):
        self.families = None
        self.individuals = None
        self.famMap = None
        self.indMap = None
        self.logger = None
        self.spousecheck = None

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
            "CHIL": ["I14", "I28", "I29", "I30"],
            "MARR": [1, 1, 2014],
            "NOTE": "PRITCHETT/TUCKER FAMILY",
            "FAM": "F4",
            "WIFE": "-"
         })
        self.families.append({
            "HUSB": ["I16"],
            "WIFE": ["I17"],
            "CHIL": ["I5", "I14"],
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
            "WIFE": ["I14"],
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
            "MARR": [16, 1, 2014],
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
            "AGE": 143,
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
            "DEAT": [14, 1, 2020],
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
            "INDI": "I14"
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
            "INDI": "I14"
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
        self.individuals.append({
            "NAME": "Sammy/Tucker-Pritchett/",
            "SEX": "M",
            "BIRT": [1, 4, 2020],
            "FAMC": ["F4"],
            "AGE": 0,
            "INDI": "I28"
         })
        self.individuals.append({
            "NAME": "Beatrice/Tucker-Pritchett/",
            "SEX": "M",
            "BIRT": [1, 4, 2020],
            "FAMC": ["F4"],
            "AGE": 0,
            "INDI": "I29"
         })
        self.individuals.append({
            "NAME": "John/Tucker-Pritchett/",
            "SEX": "M",
            "BIRT": [1, 4, 2020],
            "FAMC": ["F4"],
            "AGE": 0,
            "INDI": "I30"
         })

        for ind in self.individuals:
            self.indMap[ind["INDI"]] = ind

        for fam in self.families:
            self.famMap[fam["FAM"]] = normalize_family_entry(fam)

    def test_US32_DefaultCount(self):
        # should return F4 & F10 family with twins
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck._mult_births(32, 2)

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 2,
                         "Did not get the expected results")

        expected_ret = [
            ('Warning', 'Family', 32, 'F4 has 3 children with the same birthday (4/1/2020): I28, I29, I30'),
            ('Warning', 'Family', 32, 'F10 has 2 children with the same birthday (5/8/2019): I22, I23')
         ]
        self.assertListEqual(expected_ret, ret, "Expected Return does not match")

        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us32_mult_births()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 2,
                         "Did not get the expected results")

        expected_ret = [
            ('Warning', 'Family', 32, 'F4 has 3 children with the same birthday (4/1/2020): I28, I29, I30'),
            ('Warning', 'Family', 32, 'F10 has 2 children with the same birthday (5/8/2019): I22, I23')
         ]
        self.assertListEqual(expected_ret, ret, "Expected Return does not match")

    def test_ThreeOrMore(self):
        # should get the following families with multiple births of 3 or more
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck._mult_births(14, 3)

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 1,
                         "Did not get the expected results")

    def test_ThreeOrMoreText(self):
        # should get the following families with multiple births of 3 or more
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck._mult_births(14, 3)

        ret = self.logger.get_logs()
        expected_ret = [
            ('Warning', 'Family', 14, 'F4 has 3 children with the same birthday (4/1/2020): I28, I29, I30')
         ]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

    def test_TwoorMoreMultBirthsinOneFamiy(self):
        # add in a set of sixtuplets to family 4 - so they have triplets and twins
        for i in range(31, 37):
            self.indMap["I"+str(i)] = {
                "NAME": "I" + str(i) + "/Tucker-Pritchett/",
                "SEX": "F",
                "BIRT": [1, 5, 2019],
                "FAMC": ["F4"],
                "NOTE": "Adding Multiple Birth Child to Family F4",
                "INDI": "I" + str(i)
            }
            self.famMap["F4"]["CHIL"].append("I" + str(i))

        # private routine
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck._mult_births(33, 2)

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 3,
                         "Did not get the expected results")

        expected_ret = [
            ('Warning', 'Family', 33, 'F4 has 3 children with the same birthday (4/1/2020): I28, I29, I30'),
            ('Warning', 'Family', 33, 'F4 has 6 children with the same birthday (5/1/2019): I31, I32, I33, I34, I35, I36'),
            ('Warning', 'Family', 33, 'F10 has 2 children with the same birthday (5/8/2019): I22, I23')
         ]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

        # user story 32
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us32_mult_births()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 3,
                         "Did not get the expected results")

        expected_ret = [
            ('Warning', 'Family', 32, 'F4 has 3 children with the same birthday (4/1/2020): I28, I29, I30'),
            ('Warning', 'Family', 32, 'F4 has 6 children with the same birthday (5/1/2019): I31, I32, I33, I34, I35, I36'),
            ('Warning', 'Family', 32, 'F10 has 2 children with the same birthday (5/8/2019): I22, I23')
         ]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

        # user story 14
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us14_mult_births()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 1,
                         "Did not get the expected results")

        expected_ret = [
            ('Warning', 'Family', 14, 'F4 has 6 children with the same birthday (5/1/2019): I31, I32, I33, I34, I35, I36')
         ]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

    def test_FiveorMoreMultBirthsinOneFamiy(self):
        # add in a set of sixtuplets to family 4 - so they have triplets and twins
        for i in range(31, 36):
            self.indMap["I"+str(i)] = {
                "NAME": "I" + str(i) + "/Tucker-Pritchett/",
                "SEX": "F",
                "BIRT": [1, 5, 2019],
                "FAMC": ["F4"],
                "NOTE": "Adding Multiple Birth Child to Family F4",
                "INDI": "I" + str(i)
            }
            self.famMap["F4"]["CHIL"].append("I" + str(i))

        # user story 14
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us14_mult_births()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 0,
                         "Did not get the expected results")

        expected_ret = []
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

        # user story 32
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us32_mult_births()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 3,
                         "Did not get the expected results")

        expected_ret = [
            ('Warning', 'Family', 32, 'F4 has 3 children with the same birthday (4/1/2020): I28, I29, I30'),
            ('Warning', 'Family', 32, 'F4 has 5 children with the same birthday (5/1/2019): I31, I32, I33, I34, I35'),
            ('Warning', 'Family', 32, 'F10 has 2 children with the same birthday (5/8/2019): I22, I23')
         ]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

    def test_SixorMoreMultBirthsinOneFamiy(self):
        # add in a set of sixtuplets to family 4 - so they have triplets and twins
        for i in range(31, 37):
            self.indMap["I"+str(i)] = {
                "NAME": "I" + str(i) + "/Tucker-Pritchett/",
                "SEX": "F",
                "BIRT": [1, 5, 2019],
                "FAMC": ["F4"],
                "NOTE": "Adding Multiple Birth Child to Family F4",
                "INDI": "I" + str(i)
            }
            self.famMap["F4"]["CHIL"].append("I" + str(i))

        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck._mult_births(14, 6)

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 1,
                         "Did not get the expected results")

        expected_ret = [
            ('Warning', 'Family', 14, 'F4 has 6 children with the same birthday (5/1/2019): I31, I32, I33, I34, I35, I36')
         ]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us14_mult_births()
        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 1,
                         "Did not get the expected results")

        expected_ret = [
                ('Warning', 'Family', 14, 'F4 has 6 children with the same birthday (5/1/2019): I31, I32, I33, I34, I35, I36')
         ]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

        # user story 32
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us32_mult_births()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 3,
                         "Did not get the expected results")

        expected_ret = [
            ('Warning', 'Family', 32, 'F4 has 3 children with the same birthday (4/1/2020): I28, I29, I30'),
            ('Warning', 'Family', 32, 'F4 has 6 children with the same birthday (5/1/2019): I31, I32, I33, I34, I35, I36'),
            ('Warning', 'Family', 32, 'F10 has 2 children with the same birthday (5/8/2019): I22, I23')
         ]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

    def test_SevenorMoreMultBirthsinOneFamiy(self):
        # add in a set of sixtuplets to family 4 - so they have triplets and twins
        # won't find a match on 7
        for i in range(31, 37):
            self.indMap["I"+str(i)] = {
                "NAME": "I" + str(i) + "/Tucker-Pritchett/",
                "SEX": "F",
                "BIRT": [1, 5, 2019],
                "FAMC": ["F4"],
                "NOTE": "Adding Multiple Birth Child to Family F4",
                "INDI": "I" + str(i)
            }
            self.famMap["F4"]["CHIL"].append("I" + str(i))

        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck._mult_births(14, 7)

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 0,
                         "Did not get the expected results")

        expected_ret = []
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

        # user story 14
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us14_mult_births()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 1,
                         "Did not get the expected results")

        expected_ret = [
            ('Warning', 'Family', 14, 'F4 has 6 children with the same birthday (5/1/2019): I31, I32, I33, I34, I35, I36'),
         ]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

        # user story 32
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us32_mult_births()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 3,
                         "Did not get the expected results")

        expected_ret = [
            ('Warning', 'Family', 32, 'F4 has 3 children with the same birthday (4/1/2020): I28, I29, I30'),
            ('Warning', 'Family', 32, 'F4 has 6 children with the same birthday (5/1/2019): I31, I32, I33, I34, I35, I36'),
            ('Warning', 'Family', 32, 'F10 has 2 children with the same birthday (5/8/2019): I22, I23')
         ]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")


if __name__ == '__main__':
    unittest.main()
