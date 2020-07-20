import unittest
from datetime import datetime
from Utils.UserStory35 import born_within_one_month
from Utils.Utils import n_months_ago

class US35Test(unittest.TestCase):

    def test_born_within_one_month_valid(self):
        self.assertTrue(born_within_one_month({"BIRT": [1, 7, 2000]}, datetime(2000, 8, 1)))
        self.assertTrue(born_within_one_month({"BIRT": [1, 2, 2000]}, datetime(2000, 3, 1)))
        self.assertTrue(born_within_one_month({"BIRT": [29, 2, 2000]}, datetime(2000, 3, 30)))
        self.assertTrue(born_within_one_month({"BIRT": [28, 2, 1999]}, datetime(1999, 3, 30)))

        self.assertTrue(born_within_one_month({"BIRT": [1, 6, 2000]}, datetime(2000, 7, 1)))
        self.assertFalse(born_within_one_month({"BIRT": [1, 6, 1999]}, datetime(2000, 7, 1)))

        self.assertTrue(born_within_one_month({"BIRT": [30, 6, 2000]}, datetime(2000, 7, 1)))
        self.assertFalse(born_within_one_month({"BIRT": [30, 6, 1999]}, datetime(2000, 7, 1)))

        self.assertTrue(born_within_one_month({"BIRT": [15, 6, 2000]}, datetime(2000, 7, 1)))
        self.assertFalse(born_within_one_month({"BIRT": [15, 6, 1999]}, datetime(2000, 7, 1)))

        self.assertTrue(born_within_one_month({"BIRT": [1, 7, 2000]}, datetime(2000, 7, 1)))

        self.assertFalse(born_within_one_month({"BIRT": [2, 7, 2000]}, datetime(2000, 7, 1)))

    def test_born_within_one_month_invalid(self):
        self.assertFalse(born_within_one_month({}, "No BIRT should be caught"))
        self.assertFalse(born_within_one_month({"BIRT": [40, 40, 3000]}, "Bad date should be caught"))

        with self.assertRaises(TypeError):
            born_within_one_month({"BIRT": [1, 7, 2000]}, "Some invalid type")

    def test_n_months_ago(self):
        test_date = datetime(2020, 7, 6)
        self.assertEqual(datetime(2020, 7, 6), n_months_ago(test_date, 0))
        self.assertEqual(datetime(2020, 5, 6), n_months_ago(test_date, 2))
        self.assertEqual(datetime(2020, 1, 6), n_months_ago(test_date, 7))
        self.assertEqual(datetime(2019, 12, 6), n_months_ago(test_date, 8))
        self.assertEqual(datetime(2019, 7, 6), n_months_ago(test_date, 12))
        self.assertEqual(datetime(2010, 5, 6), n_months_ago(test_date, 122))

        test_date = datetime(2020, 7, 31)
        self.assertEqual(datetime(2020, 6, 30), n_months_ago(test_date, 1))
        self.assertEqual(datetime(2020, 5, 31), n_months_ago(test_date, 2))
        self.assertEqual(datetime(2020, 2, 29), n_months_ago(test_date, 5))
        self.assertEqual(datetime(2019, 2, 28), n_months_ago(test_date, 17))

        with self.assertRaises(ValueError):
            datetime(2020, 8, 6), n_months_ago(test_date, -1)


if __name__ == '__main__':
    unittest.main()
