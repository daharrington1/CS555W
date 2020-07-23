# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 12:44:30 2020

@author: 韩逸堃
"""

import unittest
from Utils.Logger import Logger
from Utils.spouseCrossChecker import spouseCrossChecker


class SpouseTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.individuals = {}
        self.seed_data()
        self.record = Logger()

    def tearDown(self) -> None:
        self.individuals = None
        self.record = None

    def seed_data(self):
        # seed initial testing data
        self.individuals["I1"] = {
            "NAME": "Spencer Hastings",
            "FAMS": ["F1"],
            "DEAT": [1,1,2009],
            "INDI": "I1"
         }
        self.individuals["I2"] = {
            "NAME": "Blake Hastings",
            "FAMS": ["F1"],
            "BIRT": [1,1,1976],
            "INDI": "I2"
         }


    def test_divBeforeDeat(self):
        fam1 = {"FAM": "F1", "HUSB": ["I1", "I2"], "WIFE": [], "DIV": [1,1,2020]}
        fam2 = {"FAM": "F1", "HUSB": [], "WIFE": ["I1", "I2"], "DIV": [1,1,2020]}
        fam3 = {"FAM": "F1", "HUSB": ["I1"], "WIFE": ["I2"], "DIV": [1,1,2020]}
        fam4 = {"FAM": "F1", "HUSB": ["I1"], "WIFE": ["I2"], "DIV": [1,1,2008]}
        
        self.record.clear_logs()
        checker1 = spouseCrossChecker(self.record, fam1, self.individuals)
        checker1.us06_divBeforeDeat()
        self.assertEqual(len(self.record.get_logs()), 1)
        
        checker2 = spouseCrossChecker(self.record, fam2, self.individuals)
        checker2.us06_divBeforeDeat()
        self.assertEqual(len(self.record.get_logs()), 2)
        
        checker3 = spouseCrossChecker(self.record, fam3, self.individuals)
        checker3.us06_divBeforeDeat()
        self.assertEqual(len(self.record.get_logs()), 3)
    
        checker4 = spouseCrossChecker(self.record, fam4, self.individuals)
        checker4.us06_divBeforeDeat()
        self.assertEqual(len(self.record.get_logs()), 3)
        
    def test_marr14(self):
        fam1 = {"FAM": "F1", "HUSB": ["I1", "I2"], "WIFE": [], "MARR": [1,1,1988]}
        fam2 = {"FAM": "F1", "HUSB": [], "WIFE": ["I1", "I2"], "MARR": [1,1,1988]}
        fam3 = {"FAM": "F1", "HUSB": ["I1"], "WIFE": ["I2"], "MARR": [1,1,1988]}
        fam4 = {"FAM": "F1", "HUSB": ["I1"], "WIFE": ["I2"], "MARR": [1,1,2008]}
        
        self.record.clear_logs()
        checker1 = spouseCrossChecker(self.record, fam1, self.individuals)
        checker1.us10_marrAfter14()
        self.assertEqual(len(self.record.get_logs()), 1)
        
        checker2 = spouseCrossChecker(self.record, fam2, self.individuals)
        checker2.us10_marrAfter14()
        self.assertEqual(len(self.record.get_logs()), 2)
        
        checker3 = spouseCrossChecker(self.record, fam3, self.individuals)
        checker3.us10_marrAfter14()
        self.assertEqual(len(self.record.get_logs()), 3)
        
        checker4 = spouseCrossChecker(self.record, fam4, self.individuals)
        checker4.us10_marrAfter14()
        self.assertEqual(len(self.record.get_logs()), 3)
        
if __name__ == '__main__':
    unittest.main()
