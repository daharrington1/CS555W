import unittest
from datetime import datetime
from Utils.UserStory35 import born_within_thirty_days


class US35Test(unittest.TestCase):

    def test_born_within_thirty_valid(self):

        self.assertTrue(born_within_thirty_days({"BIRT": [1, 6, 2000]}, datetime(2000, 7, 1)))
        self.assertFalse(born_within_thirty_days({"BIRT": [1, 6, 1999]}, datetime(2000, 7, 1)))

        self.assertTrue(born_within_thirty_days({"BIRT": [30, 6, 2000]}, datetime(2000, 7, 1)))
        self.assertFalse(born_within_thirty_days({"BIRT": [30, 6, 1999]}, datetime(2000, 7, 1)))

        self.assertTrue(born_within_thirty_days({"BIRT": [15, 6, 2000]}, datetime(2000, 7, 1)))
        self.assertFalse(born_within_thirty_days({"BIRT": [15, 6, 1999]}, datetime(2000, 7, 1)))

        self.assertTrue(born_within_thirty_days({"BIRT": [1, 7, 2000]}, datetime(2000, 7, 1)))

        self.assertFalse(born_within_thirty_days({"BIRT": [2, 7, 2000]}, datetime(2000, 7, 1)))

    def test_born_within_thirty_invalid(self):
        self.assertFalse(born_within_thirty_days({}, "No BIRT should be caught"))
        self.assertFalse(born_within_thirty_days({"BIRT": [40, 40, 3000]}, "Bad date should be caught"))

        with self.assertRaises(TypeError):
            born_within_thirty_days({"BIRT": [1, 7, 2000]}, "Some invalid type")



if __name__ == '__main__':
    unittest.main()
