# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 20:54:16 2020

@author: 韩逸堃
"""
from Parser.parser_checker import parser4
import unittest
from Utils.Logger import Logger


class MyTest(unittest.TestCase):
    # any kind of ahead should be detected
    def test_TwoDate(self):
        self.assertFalse(self.totest.compTwoDate([12, 9, 2020], [1, 9, 2020]))
        self.assertFalse(self.totest.compTwoDate([12, 9, 2020], [25, 8, 2020]))
        self.assertFalse(self.totest.compTwoDate([12, 9, 2020], [28, 11, 1999]))
        self.assertTrue(self.totest.compTwoDate([12, 9, 2020], [28, 9, 2020]))
        self.assertTrue(self.totest.compTwoDate([12, 9, 2020], [1, 11, 2020]))
        self.assertTrue(self.totest.compTwoDate([12, 9, 2020], [1, 9, 2080]))
        self.assertTrue(self.totest.compTwoDate([12, 9, 2020], [25, 11, 2028]))

    # all date need to be checked, dependent on the validation of 'compCurrentDate' func
    def test_dataTrav(self):
        currentComp, bmComp, bdComp = self.totest.dateCheck()
        # test error numbers
        # self.assertEqual(len(currentComp.keys()), 1)
        # self.assertEqual(len(bmComp), 2)
        # self.assertEqual(len(bdComp), 1)
        # test error types
        self.assertListEqual(currentComp['I10086'], ['BIRT', 'DEAT'])
        # self.assertListEqual(bmComp, [('F9', 'I19'), ('F128', 'I10')])
        # self.assertListEqual(bdComp, ['I128'])

    # age is less than 150
    def test_age(self):
        invalid = self.totest.add_valid_age()
        self.assertListEqual(invalid, ['I10086'])

    def setUp(self) -> None:
        self.totest = parser4("ModernFamilyTest.ged", Logger())

    def tearDown(self) -> None:
        self.totest = None


if __name__ == '__main__':
    unittest.main()
