import unittest
from Utils.UserStory28 import sort_children_by_age


class US28Test(unittest.TestCase):

    def test_sorted_children_order(self):
        test_family = {"CHIL": ["I1", "I2", "I3"]}
        test_children = {"I1": {"INDI": "I1", "AGE": 25, "NAME": "Foo"},
                         "I2": {"INDI": "I2", "AGE": 35, "NAME": "Bar"},
                         "I3": {"INDI": "I3", "AGE": 15, "NAME": "Baz"},
                         "I4": {"INDI": "I4", "AGE": 20, "NAME": "Should not appear"}}

        expected = [{"INDI": "I2", "AGE": 35, "NAME": "Bar"},
                    {"INDI": "I1", "AGE": 25, "NAME": "Foo"},
                    {"INDI": "I3", "AGE": 15, "NAME": "Baz"}]

        self.assertEqual(expected, sort_children_by_age(test_family, test_children), "Incorrect result")

    def test_find_children_no_results_is_empty(self):
        self.assertEqual([], sort_children_by_age({}, {}), "Family does not have children")
        self.assertEqual([], sort_children_by_age({}, {"I2": {"SomeKey": "SomeValue"}}),
                         "Families children not in individuals")


if __name__ == '__main__':
    unittest.main()
