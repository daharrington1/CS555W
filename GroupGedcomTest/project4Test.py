# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 20:54:16 2020

@author: 韩逸堃
"""
from Parser.parserV4 import parser4
import unittest
from Utils.Logger import Logger


class MyTest(unittest.TestCase):
    #any kind of ahead should be detected
    def test_compCurrentDate(self):
        #retrieve current date: same month but with a day before
        self.assertFalse(self.totest.compCurrentDate([12,9,2020]))
        self.assertFalse(self.totest.compCurrentDate([1,6,2021]))
        self.assertFalse(self.totest.compCurrentDate([28,9,2021]))
        self.assertTrue(self.totest.compCurrentDate([28,6,1987]))
        self.assertTrue(self.totest.compCurrentDate([28,12,1996]))
    
    #all date need to be checked, dependent on the validation of 'compCurrentDate' func
    def test_dataTrav(self):
        toComp = self.totest.dateCheck()
        #test error types
        self.assertListEqual(toComp['I1'], ['BIRT'])
        self.assertListEqual(toComp['I3'], ['DEAT'])
        self.assertListEqual(toComp['F2'], ['MARR', 'DIV'])
        #test the error numbers
        length = len(toComp.keys())
        #print(length, type(length))
        self.assertEqual(length, 5)
    
    #age is less than 150
    def test_age(self):
        invalid = self.totest.add_valid_age()
        self.assertListEqual(invalid, ['I3'])

    def setUp(self) -> None:
        self.totest = parser4("ModernFamilyTest.ged", Logger())

    def tearDown(self) -> None:
        self.totest = None


if __name__ == '__main__':
    unittest.main()


