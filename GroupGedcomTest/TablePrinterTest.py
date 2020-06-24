import unittest

from mockito import mock, when
import sys
sys.path.append('../TablePrinter')
from TablePrinter import TablePrinter


class TablePrinterTest(unittest.TestCase):
    _testPrinter = None
    _mockDatabase = None

    def setUp(self):
        self._mockDatabase = mock()
        self._testPrinter = TablePrinter(self._mockDatabase)

    def tearDown(self):
        self._testPrinter = None
        self._mockDatabase = None

    def testIndividualFormatting(self):
        input_individuals = [
            {'INDI': 'I1', 'SEX': 'M', 'FAMS': ['F1', 'F2'], 'BIRT': [23, 5, 1947], 'NAME': 'Jay /Pritchett/'}]

        formatted_table = self._testPrinter.format_individuals(input_individuals)
        expected_table = \
            "Individuals\n" \
            "+----+-----------------+--------+------------+------+-------+-------+----------+-----------+\n" \
            "| Id |      Name       | Gender |  Birthday  |  Age | Alive | Death | Child Id | Spouse Id |\n" \
            "+----+-----------------+--------+------------+------+-------+-------+----------+-----------+\n" \
            "| I1 | Jay /Pritchett/ |   M    | 23/05/1947 |  -   | True  |  N/A  |   N/A    |   F1,F2   |\n" \
            "+----+-----------------+--------+------------+------+-------+-------+----------+-----------+"
        self.assertEqual(expected_table, formatted_table, "Table did not matched formatted exactly")

    def testIndividualMissingIdRaises(self):
        test_dictionary = {'SEX': 'M', 'FAMS': ['F1', 'F2'], 'BIRT': [23, 5, 1947], 'NAME': 'Jay /Pritchett/'}
        with self.assertRaises(KeyError):
            self._testPrinter.format_individuals([test_dictionary])

    def testIndividualMissingNameRaises(self):
        test_dictionary = {'INDI': 'I1', 'SEX': 'M', 'FAMS': ['F1', 'F2'], 'BIRT': [23, 5, 1947]}
        with self.assertRaises(KeyError):
            self._testPrinter.format_individuals([test_dictionary])

    def testIndividualMissingSexRaises(self):
        test_dictionary = {'INDI': 'I1', 'FAMS': ['F1', 'F2'], 'BIRT': [23, 5, 1947], 'NAME': 'Jay /Pritchett/'}
        with self.assertRaises(KeyError):
            self._testPrinter.format_individuals([test_dictionary])

    def testIndividualMissingBirtRaises(self):
        test_dictionary = {'INDI': 'I1', 'SEX': 'M', 'FAMS': ['F1', 'F2'], 'NAME': 'Jay /Pritchett/'}
        with self.assertRaises(KeyError):
            self._testPrinter.format_individuals([test_dictionary])

    def testOnlyIndividualRequiredKeysDoesNotRaise(self):
        test_dictionary = {'INDI': 'I1', 'SEX': 'M', 'BIRT': [23, 5, 1947], 'NAME': 'Jay /Pritchett/'}
        formatted = self._testPrinter.format_individuals([test_dictionary])
        self.assertNotEqual(self._testPrinter.format_individuals([]), formatted, "Should not be empty table")

    def testFormatOfFamilyTable(self):
        when(self._mockDatabase).getName('I1').thenReturn("Joe /Pritchett/")
        when(self._mockDatabase).getName('I3').thenReturn("DeDe /Pritchett/")
        formatted = self._testPrinter.format_families([{'HUSB': ['I1'],
                                                        'MARR': [1, 1, 1968], 'CHIL': ['I4', 'I6'], 'WIFE': ['I3'],
                                                        'FAM': 'F2', 'DIV': [1, 1, 2003]}])

        # Ugly table formatting, but unable to hide line to long warnings on multi line literals
        expected = \
            "Families\n+----+------------+------------+------------+-----------------+---------+------------------+" \
            "--------------+\n| Id |  Married   |  Divorced  | Husband Id |  Husband Name   | Wife Id |    Wife Name" \
            "     | Children Ids |\n+----+------------+------------+------------+-----------------+---------+--------" \
            "----------+--------------+\n| F2 | 01/01/1968 | 01/01/2003 |     I1     | Joe /Pritchett/ |   I3    | " \
            "DeDe /Pritchett/ |    I4,I6     |\n+----+------------+------------+------------+-----------------+------" \
            "---+------------------+--------------+"
        self.assertEqual(expected, formatted, "Family output did not expected ")

    def testMissingFamIdRaises(self):
        test_dictionary = {'HUSB': ['I1'],
                           'MARR': [1, 1, 1968], 'CHIL': ['I4', 'I6'], 'WIFE': ['I3'],
                           'DIV': [1, 1, 2003]}
        with self.assertRaises(KeyError):
            self._testPrinter.format_families([test_dictionary])

    def testFamilyMissingFamIdRaises(self):
        test_dictionary = {'HUSB': ['I1'], 'MARR': [1, 1, 1968], 'CHIL': ['I4', 'I6'],
                           'WIFE': ['I3'], 'DIV': [1, 1, 2003]}
        with self.assertRaises(KeyError):
            self._testPrinter.format_families([test_dictionary])

    def testFamilyMissingMarrKeyRaises(self):
        test_dictionary = {'FAM': 'F2', 'HUSB': ['I1'], 'CHIL': ['I4', 'I6'], 'WIFE': ['I3'], 'DIV': [1, 1, 2003]}
        with self.assertRaises(KeyError):
            self._testPrinter.format_families([test_dictionary])

    def testFamilyMissingHUSBKeyRaise(self):
        test_dictionary = {'FAM': 'F2', 'MARR': [1, 1, 1968], 'CHIL': ['I4', 'I6'],
                           'WIFE': ['I3'], 'DIV': [1, 1, 2003]}
        with self.assertRaises(KeyError):
            self._testPrinter.format_families([test_dictionary])

    def testFamilyMissingWIFEKeyRaise(self):
        test_dictionary = {'FAM': 'F2', 'HUSB': ['I1'], 'MARR': [1, 1, 1968],
                           'CHIL': ['I4', 'I6'], 'DIV': [1, 1, 2003]}
        with self.assertRaises(KeyError):
            self._testPrinter.format_families([test_dictionary])

    def testOnlyRequiredFamilyKeysDoNotRaise(self):
        when(self._mockDatabase).getName('I1').thenReturn("Joe /Pritchett/")
        when(self._mockDatabase).getName('I3').thenReturn("DeDe /Pritchett/")
        test_dictionary = {'FAM': 'F2', 'HUSB': ['I1'], 'MARR': [1, 1, 1968], 'WIFE': ['I3']}
        result = self._testPrinter.format_families([test_dictionary])
        self.assertNotEqual(self._testPrinter.format_families([]), result, "Returned empty table")

    def testValidDateMapping(self):
        self.assertEqual("01/01/2000", self._testPrinter.format_date([1, 1, 2000]))
        self.assertEqual("01/10/2001", self._testPrinter.format_date([1, 10, 2001]))
        self.assertEqual("10/31/0023", self._testPrinter.format_date([10, 31, 23]))
        self.assertEqual("07/17/2010", self._testPrinter.format_date([7, 17, 2010]))

    def testInvalidSyntaxDateMappings(self):
        self.assertEqual("-", self._testPrinter.format_date([1, 3]))
        self.assertEqual("-", self._testPrinter.format_date(None))
        self.assertEqual("-", self._testPrinter.format_date({"someKey": "someValue"}))
        self.assertEqual("-", self._testPrinter.format_date((1, 2, 3)))


if __name__ == '__main__':
    unittest.main()
