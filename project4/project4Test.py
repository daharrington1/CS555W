# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 20:54:16 2020

@author: 韩逸堃
"""
from parserV4 import parser4
import unittest

class MyTest(unittest.TestCase):
    #any kind of ahead should be detected
    def compCurrentDate_test(self):
        self.assertFalse(self.totest.compCurrentDate([28,6,2020]))
        self.assertFalse(self.totest.compCurrentDate([12,9,2020]))
        self.assertFalse(self.totest.compCurrentDate([1,6,2021]))
        self.assertFalse(self.totest.compCurrentDate([28,9,2021]))
        self.assertTrue(self.totest.compCurrentDate([28,6,1987]))
        self.assertTrue(self.totest.compCurrentDate([28,12,1996]))
    
    #all date need to be checked, dependent on the validation of 'compCurrentDate' func
    def dateTrav_test(self):
        toComp = self.totest.dateCheck()
        #test error types
        self.assertListEqual(toComp['I1'], ['BIRT'])
        self.assertListEqual(toComp['I3'], ['DEAT'])
        self.assertListEqual(toComp['F2'], ['MARR', 'DIV'])
        #test the error numbers
        #length = len(list(toComp.keys()))
        #print(length, type(length))
        #self.assertEqual(length, 3)
    
    #age is less than 150
    def age_test(self):
        invalid = self.totest.add_valid_age()
        self.assertListEqual(invalid, ['I3'])
        
    def __init__(self, parsed_dic):
        self.totest = parsed_dic
        
        


project4test = MyTest(parser4("ModernFamilyTest.txt"))
project4test.compCurrentDate_test()
project4test.dateTrav_test()
project4test.age_test()


