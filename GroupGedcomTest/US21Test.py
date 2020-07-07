import unittest
from Utils.UserStory21 import filter_differing_sex, find_mistitled_spouse


class US21Test(unittest.TestCase):

    def test_filter_differing_sex(self):
        test_data = [{"INDI": "I1", "SEX": "M"}, {"INDI": "I2", "SEX": "F"},
                     {"INDI": "I3", "SEX": "F"}, {"INDI": "I4", "SEX": "M"}]

        self.assertEqual(["I1", "I4"], filter_differing_sex(test_data, "F"), "Did not find all men")
        self.assertEqual(["I2", "I3"], filter_differing_sex(test_data, "M"), "Did not find all women")
        self.assertEqual(["I1", "I2", "I3", "I4"], filter_differing_sex(test_data, "Some invalid string"),
                         "Did not return all on bad input")

    def test_find_mistitled_spouse(self):
        test_individuals = {"I1": {"INDI": "I1", "SEX": "M"}, "I2": {"INDI": "I2", "SEX": "F"},
                            "I3": {"INDI": "I3", "SEX": "M"}, "I4": {"INDI": "I4", "SEX": "F"},
                            "I5": {"INDI": "I5", "SEX": "M"}, "I6": {"INDI": "I6", "SEX": "F"}}
        test_families = [{"HUSB": ["I1"], "WIFE": ["I2"]}, {"HUSB": ["I4"], "WIFE": ["I3"]},
                         {"HUSB": ["I1"], "WIFE": ["I5"]}, {"HUSB": ["I6"], "WIFE": ["I2"]}]
        results = find_mistitled_spouse(test_individuals, test_families)
        self.assertEqual(4, len(results), "Possible duplicates which will be lost on set conversion")
        self.assertEqual({"I3", "I4", "I5", "I6"}, set(results), "Incorrect ids returned")


if __name__ == '__main__':
    unittest.main()
