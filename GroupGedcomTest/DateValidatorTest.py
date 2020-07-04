import unittest
from Utils.DateValidator import DateValidator
from Utils.Logger import Logger
from Utils.DateValidator import is_leap_year, format_date


class DateValidatorTest(unittest.TestCase):
    _test_validator = None

    def setUp(self):
        self._test_validator = DateValidator(Logger())

    def tearDown(self):
        self._test_validator = None

    def test_is_leap_year(self):
        self.assertTrue(is_leap_year(2000))
        self.assertTrue(is_leap_year(2004))
        self.assertTrue(is_leap_year(2008))
        self.assertTrue(is_leap_year(2012))
        self.assertTrue(is_leap_year(2016))
        self.assertTrue(is_leap_year(2020))

        self.assertFalse(is_leap_year(1900))
        self.assertFalse(is_leap_year(1901))
        self.assertFalse(is_leap_year(1902))
        self.assertFalse(is_leap_year(1903))

    def test_valid_dates(self):
        self.assertTrue(self._test_validator.validate_date([1, 1, 2000]))
        self.assertTrue(self._test_validator.validate_date([31, 1, 2000]), "31st marked invalid")
        self.assertTrue(self._test_validator.validate_date([29, 2, 2020]), "Leap year missed")
        self.assertTrue(self._test_validator.validate_date([31, 3, 2000]))
        self.assertTrue(self._test_validator.validate_date([30, 4, 2000]))
        self.assertTrue(self._test_validator.validate_date([31, 5, 2000]))
        self.assertTrue(self._test_validator.validate_date([30, 6, 2000]))
        self.assertTrue(self._test_validator.validate_date([31, 7, 2000]))
        self.assertTrue(self._test_validator.validate_date([31, 8, 2000]))
        self.assertTrue(self._test_validator.validate_date([30, 9, 2000]))
        self.assertTrue(self._test_validator.validate_date([31, 10, 2000]))
        self.assertTrue(self._test_validator.validate_date([30, 11, 2000]))
        self.assertTrue(self._test_validator.validate_date([31, 12, 2000]))

        self.assertTrue(self._test_validator.validate_date([29, 5, 2000]))
        self.assertTrue(self._test_validator.validate_date([29, 5, 2002]), "Applied leap year logic to not February")

    def test_invalid_dates(self):
        self.assertFalse(self._test_validator.validate_date([0, 1, 2000]))
        self.assertFalse(self._test_validator.validate_date([-5, 5, 2000]))
        self.assertFalse(self._test_validator.validate_date([5, 0, 2000]))
        self.assertFalse(self._test_validator.validate_date([10, "Some String", 2000]))

        self.assertFalse(self._test_validator.validate_date([32, 1, 2000]))
        self.assertFalse(self._test_validator.validate_date([30, 2, 2000]))
        self.assertFalse(self._test_validator.validate_date([29, 2, 2002]))
        self.assertFalse(self._test_validator.validate_date([32, 3, 2000]))
        self.assertFalse(self._test_validator.validate_date([31, 4, 2000]))
        self.assertFalse(self._test_validator.validate_date([32, 5, 2000]))
        self.assertFalse(self._test_validator.validate_date([31, 6, 2000]))
        self.assertFalse(self._test_validator.validate_date([32, 7, 2000]))
        self.assertFalse(self._test_validator.validate_date([32, 8, 2000]))
        self.assertFalse(self._test_validator.validate_date([31, 9, 2000]))
        self.assertFalse(self._test_validator.validate_date([32, 10, 2000]))
        self.assertFalse(self._test_validator.validate_date([31, 11, 2000]))
        self.assertFalse(self._test_validator.validate_date([32, 12, 2000]))

    def testValidDateMapping(self):
        self.assertEqual("01/01/2000", format_date([1, 1, 2000], "-"))
        self.assertEqual("01/10/2001", format_date([1, 10, 2001], "-"))
        self.assertEqual("10/31/0023", format_date([10, 31, 23], "-"))
        self.assertEqual("07/17/2010", format_date([7, 17, 2010], "-"))

    def testInvalidSyntaxDateMappings(self):
        self.assertEqual("-", format_date([1, 3], "-"))
        self.assertEqual("-", format_date(None, "-"))
        self.assertEqual("-", format_date({"someKey": "someValue"}, "-"))
        self.assertEqual("-", format_date((1, 2, 3), "-"))


if __name__ == '__main__':
    unittest.main()
