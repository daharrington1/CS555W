import unittest
from Utils.UserStory33 import younger_than, all_spouses_dead, find_all_orphans


class US33Test(unittest.TestCase):
    def test_younger_than_valid_data(self):
        individuals = {"I1": {"AGE": 16}, "I2": {"AGE": 20}, "I3": {"AGE": 4}, "I4": {"AGE": 24}, "I5": {"AGE": 18}}

        self.assertEqual([], younger_than(18, individuals, []), "No targets specified")
        self.assertEqual(["I1", "I3"],
                         younger_than(18, individuals, ["I1", "I2", "I3", "I4", "I5", ]), "Wrong Values returned")

    def test_younger_than_invalid_data(self):
        with self.assertRaises(KeyError):
            younger_than(18, {}, ["I1", "I2", "I3", "I4", "I5", ])

    def test_all_dead(self):
        family = {"HUSB": "I1", "WIFE": "I2"}
        test_ids = {"I1": {"DEAT": "someVal"}, "I2": {"DEAT": "someVal"}}
        self.assertTrue(all_spouses_dead(test_ids, family))

        family = {"HUSB": ["I1", "I2"]}
        self.assertTrue(all_spouses_dead(test_ids, family))

        family = {"WIFE": ["I1", "I2"]}
        self.assertTrue(all_spouses_dead(test_ids, family))

        family = {"HUSB": "I1", "WIFE": "I2"}

        test_ids = {"I1": {"DEAT": "someVal"}, "I2": {}}
        self.assertFalse(all_spouses_dead(test_ids, family))

        test_ids = {"I1": {}, "I2": {"DEAT": "someVal"}}
        self.assertFalse(all_spouses_dead(test_ids, family))

        test_ids = {"I1": {}, "I2": {}}
        self.assertFalse(all_spouses_dead(test_ids, family))

    def test_find_orphans(self):
        test_families = [{"HUSB": "I1", "WIFE": "I2", "CHIL": ["I9"]}, {"HUSB": ["I3", "I4"], "CHIL": []},
                         {"HUSB": "I5", "WIFE": "I6", "CHIL": ["I10", "I11"]}, {"WIFE": ["I7", "I8"], "CHIL": []}]

        test_ids = [{"INDI": "I1", "DEAT": "someVal"}, {"INDI": "I2"}, {"INDI": "I3", "DEAT": "someVal"},
                    {"INDI": "I4"}, {"INDI": "I5", "DEAT": "someVal"}, {"INDI": "I6", "DEAT": "someVal"},
                    {"INDI": "I7", "DEAT": "someVal"}, {"INDI": "I8", "DEAT": "someVal"}, {"INDI": "I9"},
                    {"INDI": "I10", "AGE": 18}, {"INDI": "I11", "AGE": 14}]

        self.assertEqual([["I11"]], find_all_orphans(test_ids, test_families), "Results are not orphans... yay?")

    def test_find_orphans_no_results(self):
        test_families = [{"HUSB": "I1", "WIFE": "I2", "CHIL": ["I9"]}, {"HUSB": ["I3", "I4"], "CHIL": []},
                         {"HUSB": "I5", "WIFE": "I6", "CHIL": ["I10", "I11"]}, {"WIFE": ["I7", "I8"], "CHIL": []}]

        test_ids = [{"INDI": "I1", "DEAT": "someVal"}, {"INDI": "I2"}, {"INDI": "I3", "DEAT": "someVal"},
                    {"INDI": "I4"}, {"INDI": "I5", "DEAT": "someVal"}, {"INDI": "I6", "DEAT": "someVal"},
                    {"INDI": "I7", "DEAT": "someVal"}, {"INDI": "I8", "DEAT": "someVal"}, {"INDI": "I9"},
                    {"INDI": "I10", "AGE": 18}, {"INDI": "I11", "AGE": 24}]
        self.assertEqual([], find_all_orphans(test_ids, test_families), "Empty list was not flattened")

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
