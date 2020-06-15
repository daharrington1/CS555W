import unittest
from db.db_interface import GenComDb
from Utils import us17_no_marr2child
import json, sys, pprint


class US17Test(unittest.TestCase):
    coll_fam = None
    db_ind = None

    def setUp(self):
        # drop the individuals database just in case it is there
        self.db_ind=GenComDb(GenComDb.MONGO_INDIVIDUALS)
        self.db_ind.dropCollection()

        self.coll_fam=GenComDb(GenComDb.MONGO_FAMILIES)
        self.coll_fam.dropCollection()

        self.seed_data()

    def tearDown(self):
        self.db_ind.dropCollection()
        self.db_ind = None

        self.coll_fam.dropCollection()
        self.coll_fam = None

    def seed_data(self):
        # seed family data - don't need individual data for this test suite

        fam = { "HUSB" : [ "I1" ], "WIFE" : [ "I2" ], "CHIL" : [ "I10" ], "MARR" : [ 1, 1, 2009 ],  "NOTE" : "JAY/GLORIA FAMILY", "FAM" : "F1" }
        self.coll_fam.AddObj(fam)
        fam = { "HUSB" : [ "I1" ], "WIFE" : [ "I3" ], "CHIL" : [ "I4", "I6" ], "MARR" : [ 1, 1, 1968 ], "DIV" : [ 1, 1, 2003 ], "NOTE" : "JAY/DEEDEE FAMILY", "FAM" : "F2" }
        self.coll_fam.AddObj(fam)
        fam = { "HUSB" : [ "I8" ], "WIFE" : [ "I2" ], "CHIL" : [ "I9" ], "MARR" : [ 1, 1, 1995 ], "DIV" : [ 1, 1, 2006 ], "NOTE" : "JAVIER/GLORIA FAMILY", "FAM" : "F3" }
        self.coll_fam.AddObj(fam)
        fam = { "HUSB" : [ "I4", "I5" ], "CHIL" : [ "I14", "I15" ], "MARR" : [ 1, 1, 2014 ], "NOTE" : "MITCHELL/CAMERON FAMILY", "FAM" : "F4", "WIFE" : "-" }
        self.coll_fam.AddObj(fam)
        fam = { "HUSB" : [ "I16" ], "WIFE" : [ "I17" ], "CHIL" : [ "I5", "I18" ], "MARR" : [ 1, 1, 1963 ], "NOTE" : "MERLE/BARE FAMILY", "FAM" : "F5" }
        self.coll_fam.AddObj(fam)
        fam = { "HUSB" : [ "I7" ], "WIFE" : [ "I6" ], "CHIL" : [ "I20", "I24", "I25" ], "MARR" : [ 1, 4, 1993 ], "NOTE" : "DUNPHY/PRITCHETT FAMILY", "FAM" : "F6" }
        self.coll_fam.AddObj(fam)
        fam = { "HUSB" : [ "I11" ], "WIFE" : [ "I13" ], "CHIL" : [ "I7" ], "MARR" : [ 1, 1, 1965 ], "NOTE" : "FRANK/GRACE FAMILY", "FAM" : "F7" } 
        self.coll_fam.AddObj(fam)
        fam = { "HUSB" : [ "I11" ], "WIFE" : [ "I12" ], "MARR" : [ 5, 4, 2017 ], "NOTE" : "FRANK/LORRAINE", "FAM" : "F8" }
        self.coll_fam.AddObj(fam)
        fam = { "WIFE" : [ "I18" ], "CHIL" : [ "I19" ], "NOTE" : "HALEY/DILLON FAMILY", "FAM" : "F9", "MARR" : "-", "HUSB" : "-" , "NOTE" : "PAMERON FAMILY"}
        self.coll_fam.AddObj(fam)
        fam = { "HUSB" : [ "I21" ], "WIFE" : [ "I20" ], "CHIL" : [ "I22", "I23" ], "MARR" : [ 8, 3, 2019 ], "TRLR" : "", "FAM" : "F10" , "NOTE" : "DYLAN/HALEY FAMILY"}
        self.coll_fam.AddObj(fam)
	

    def test_US17_wrongdb(self):

        #call on wrong collection
        with self.assertRaises(Exception) as context:
            ret=us17_no_marr2child(self.coll_ind)

    def test_US17_nomatches(self):
        # expect 2 get 2 matches
        ret=us17_no_marr2child(self.coll_fam)
        self.assertEqual(len(ret), 0, "Did not get the expected results")

    def test_US17_nocollection(self):
        # drop the collection
        self.coll_fam.dropCollection()

        # expect 2 get 2 matches
        ret=us17_no_marr2child(self.coll_fam)
        self.assertEqual(len(ret), 0, "Did not get the expected results")

    def test_US17_1family(self):
        #should to get 1 match
        self.coll_fam.updateId("F4", "CHIL", ['I14', 'I15', 'I5'])
        ret=us17_no_marr2child(self.coll_fam)
        self.assertEqual(len(ret), 1, "Did not get the expected results")

    def test_US17_1family_text(self):
        #should find 1 match and the following expected result
        expected_ret=[{'HUSB': ['I4', 'I5'], 'CHIL': ['I14', 'I15', 'I5'], 'FAM': 'F4', 'WIFE': '-', 'MarriagetoChildren': ['I5']}]
        self.coll_fam.updateId("F4", "CHIL", ['I14', 'I15', 'I5'])
        ret=us17_no_marr2child(self.coll_fam)
        self.assertListEqual(expected_ret, ret, "Expected Return does not match")


    def test_US17_2families(self):
        #should to get 2 matches- one with same sex marraige, one without
        self.coll_fam.updateId("F4", "CHIL", ['I14', 'I15', 'I5'])
        self.coll_fam.updateId("F5", "CHIL", ['I5', 'I18', 'I17'])
        ret=us17_no_marr2child(self.coll_fam)
        self.assertEqual(len(ret), 2, "Did not get the expected results")


    def test_US17_2families_text(self):
        #should find 2 matches and the following expected result- one with same sex marraige, one without
        expected_ret=[{'HUSB': ['I4', 'I5'], 'CHIL': ['I14', 'I15', 'I5'], 'FAM': 'F4', 'WIFE': '-', 'MarriagetoChildren': ['I5']},{'HUSB': ['I16'], 'WIFE': ['I17'], 'CHIL': ['I5', 'I18', 'I17'], 'FAM': 'F5', 'MarriagetoChildren': ['I17']}]
        self.coll_fam.updateId("F4", "CHIL", ['I14', 'I15', 'I5'])
        self.coll_fam.updateId("F5", "CHIL", ['I5', 'I18', 'I17'])
        ret=us17_no_marr2child(self.coll_fam)
        self.assertListEqual(expected_ret, ret, "Expected Return does not match")











	

if __name__ == '__main__':
    unittest.main()
