import unittest
import datetime
from Utils.UserStory13 import find_invalid_sibling_spacing


class US13Test(unittest.TestCase):

    def test_find_invalid_sibling_spacing(self):
        test_individuals = {"I1": {"INDI": "I1", "BIRT": [4, 6, 2020]}, "I2": {"INDI": "I2", "BIRT": [2, 6, 2020]},
                            "I3": {"INDI": "I3", "BIRT": [2, 6, 2020]}, "I5": {"INDI": "I5", "BIRT": [30, 6, 2020]},
                            "I6": {"INDI": "I6", "BIRT": [31, 1, 2020]}, "I7": {"INDI": "I7", "BIRT": [30, 10, 20]},
                            "I8": {"INDI": "I8", "BIRT": [1, 4, 2020]}, "I9": {"INDI": "I9", "BIRT": [7, 7, 2020]},
                            "I10": {"INDI": "I10", "BIRT": [8, 7, 2020]}}
        test_families = [{"CHIL": ["I1", "I2"]}, {"CHIL": ["I3"]}, {}, {"CHIL": ["I5", "I6"]}, {"CHIL": ["I7", "I8"]},
                         {"CHIL": ["I9", "I10"]}]
        result = find_invalid_sibling_spacing(test_individuals, test_families)
        self.assertEqual({"I1", "I2", "I5", "I6"}, set(find_invalid_sibling_spacing(test_individuals, test_families)))
        self.assertEqual(4, len(result), "Wrong length, might contain dupes or missing data")

        self.assertEqual(set(), find_invalid_sibling_spacing(test_individuals, {}))

if __name__ == '__main__':
    unittest.main()
