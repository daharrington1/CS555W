import unittest
from Utils.Logger import Logger
from Utils.spouseCrossChecker import spouseCrossChecker
import datetime


#
# Test Scripts for User Story 39: upcoming anniversaries
# Author: Debbie Harrington
#
# Test Scripts for verifying US39 user story
# Base everything off of today's date - so the test scripts work.
#

class US39Test(unittest.TestCase):
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
            "HUSB": ["I4", "I5"],
            "CHIL": ["I14", "I15"],
            "MARR": [1, 1, 2014],
            "NOTE": "PRITCHETT/TUCKER FAMILY",
            "FAM": "F4",
            "WIFE": "-"
         })
        self.families.append({
            "HUSB": ["I11"],
            "WIFE": ["I12"],
            "MARR": [5, 4, 2039],
            "NOTE": "FRANK/LORRAINE FAMILY ",
            "FAM": "F8"
         })
        self.families.append({
            "HUSB": ["I21"],
            "WIFE": ["I20"],
            "CHIL": ["I22", "I23"],
            "MARR": [8, 3, 2019],
            "FAM": "F10",
            "NOTE": "MARSHALL/DUNPHY FAMILY"
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
            "NAME": "Lorraine/Dunphy/",
            "SEX": "F",
            "BIRT": [1, 1, 1965],
            "FAMS": ["F8"],
            "AGE": 55,
            "INDI": "I12"
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

        for ind in self.individuals:
            self.indMap[ind["INDI"]] = ind

        for fam in self.families:
            self.famMap[fam["FAM"]] = fam

    def test_US39_noMatches(self):
        # should no matches
        self.logger.clear_logs()
        for id, fam in self.famMap.items():
            # overwrite all Marriages as one day ago
            dt = datetime.date.today()-datetime.timedelta(days=1)
            #self.famMap[id]["MARR"] = []
            #self.famMap[id]["MARR"] = [dt.day, dt.month, dt.year]
            #us39_upcoming_anniversaries(self.indMap, fam, self.logger)
            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 0, "Did not get the expected results")

    def test_US39_1dayLaterLen(self):
        # should no matches

        self.logger.clear_logs()
        for id, fam in self.famMap.items():

            if id == "F10":
                dt = datetime.date.today()+datetime.timedelta(days=1)
            else:
                dt = datetime.date.today()-datetime.timedelta(days=1)

            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 1, "Did not get the expected results")

    def test_US39_1dayLater(self):
        # should no matches
        self.logger.clear_logs()
        for id, fam in self.famMap.items():

            if id == "F10":
                dt = datetime.date.today()+datetime.timedelta(days=1)
            else:
                dt = datetime.date.today()-datetime.timedelta(days=1)

            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        # should find 1 match and the following expected result
        ret = self.logger.get_logs()
        dtstr = 'FAMILY (F10) has an upcoming anniversary: '+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.year)
        expected_ret = [('Info', 'Family', 39, dtstr)]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

    def test_US39_30daysLaterLen(self):
        # should no matches
        self.logger.clear_logs()
        for id, fam in self.famMap.items():

            if id == "F10":
                dt = datetime.date.today()+datetime.timedelta(days=30)
            else:
                dt = datetime.date.today()-datetime.timedelta(days=1)

            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 1, "Did not get the expected results")

    def test_US39_30daysLater(self):
        # should no matches
        self.logger.clear_logs()
        for id, fam in self.famMap.items():

            if id == "F10":
                dt = datetime.date.today()+datetime.timedelta(days=30)
            else:
                dt = datetime.date.today()-datetime.timedelta(days=1)

            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        # should find 1 match and the following expected result
        ret = self.logger.get_logs()
        dtstr = 'FAMILY (F10) has an upcoming anniversary: '+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.year)
        expected_ret = [('Info', 'Family', 39, dtstr)]
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

    def test_US39_31daysLaterLen(self):
        # should no matches
        self.logger.clear_logs()
        for id, fam in self.famMap.items():

            if id == "F10":
                dt = datetime.date.today()+datetime.timedelta(days=31)
            else:
                dt = datetime.date.today()-datetime.timedelta(days=1)

            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 0, "Did not get the expected results")

    def test_US39_31daysLater(self):
        # should no matches
        self.logger.clear_logs()
        for id, fam in self.famMap.items():

            if id == "F10":
                dt = datetime.date.today()+datetime.timedelta(days=31)
            else:
                dt = datetime.date.today()-datetime.timedelta(days=1)

            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        # should find 1 match and the following expected result
        ret = self.logger.get_logs()
        expected_ret = []
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

    def test_US39_2DatesUpcomingLen(self):
        # should get 2 matches
        self.logger.clear_logs()
        expected_ret = []
        for id, fam in self.famMap.items():

            if id == "F10":
                dt = datetime.date.today()+datetime.timedelta(days=30)
                dtstr = 'FAMILY (F10) has an upcoming anniversary: '+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.year)
                expected_ret.append(('Info', 'Family', 39, dtstr))
            elif id == "F4":
                dt = datetime.date.today()+datetime.timedelta(days=1)
                dtstr = 'FAMILY (F4) has an upcoming anniversary: '+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.year)
                expected_ret.append(('Info', 'Family', 39, dtstr))
            else:
                # overwrite all Marriages as one day ago
                dt = datetime.date.today()-datetime.timedelta(days=1)

            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 2, "Did not get the expected results")

    def test_US39_2DatesUpcoming(self):
        # should get 2 matches
        self.logger.clear_logs()
        expected_ret = []
        for id, fam in self.famMap.items():

            if id == "F10":
                dt = datetime.date.today()+datetime.timedelta(days=30)
                dtstr = 'FAMILY (F10) has an upcoming anniversary: '+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.year)
                expected_ret.append(('Info', 'Family', 39, dtstr))
            elif id == "F4":
                dt = datetime.date.today()+datetime.timedelta(days=1)
                dtstr = 'FAMILY (F4) has an upcoming anniversary: '+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.year)
                expected_ret.append(('Info', 'Family', 39, dtstr))
            else:
                dt = datetime.date.today()-datetime.timedelta(days=1)

            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        # should find 1 match and the following expected result
        ret = self.logger.get_logs()
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")

    def test_US39_2DatesUpcoming1WidowerLen(self):
        # should no matches
        self.logger.clear_logs()
        expected_ret = []
        for id, fam in self.famMap.items():

            if id == "F10":
                dt = datetime.date.today()+datetime.timedelta(days=30)
                dtstr = 'FAMILY (F10) has an upcoming anniversary: '+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.year)
                expected_ret.append(('Info', 'Family', 39, dtstr))
            elif id == "F8":
                dt = datetime.date.today()+datetime.timedelta(days=1)
            else:
                dt = datetime.date.today()-datetime.timedelta(days=1)

            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        ret = self.logger.get_logs()
        self.assertEqual(len(ret), 1, "Did not get the expected results")

    def test_US39_2DatesUpcoming1Widower(self):
        self.logger.clear_logs()
        expected_ret = []
        for id, fam in self.famMap.items():

            if id == "F10":
                dt = datetime.date.today()+datetime.timedelta(days=30)
                dtstr = 'FAMILY (F10) has an upcoming anniversary: '+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.year)
                expected_ret.append(('Info', 'Family', 39, dtstr))
            elif id == "F8":
                dt = datetime.date.today()+datetime.timedelta(days=1)
            else:
                dt = datetime.date.today()-datetime.timedelta(days=1)

            fam["MARR"] = [dt.day, dt.month, dt.year]
            spousecheck = spouseCrossChecker(self.logger, fam, self.indMap)
            spousecheck.us39_upcoming_anniversaries()

        ret = self.logger.get_logs()
        self.assertListEqual(expected_ret, ret,
                             "Expected Return does not match")


if __name__ == '__main__':
    unittest.main()
