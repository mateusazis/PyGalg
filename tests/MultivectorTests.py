# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:25:52 2013

@author: mateus
"""
import sys
sys.path.append("../src")

from Multivector import Multivector
import unittest

class MultivectorTests(unittest.TestCase):
    def setUp(self):
        self.zero = Multivector(coef=0, bitmap=0)
        
    def test_ex2_a1(self):
        #e1 ^ (e1 ^ e2 ^ e4) = 0
        first = Multivector(bitmap=0b0001)
        
        second = Multivector(bitmap=0b1011)
        
        self.assertEquals(self.zero, first ^ second)
        
    def test_ex2_a2(self):
        #e1 ^ (e1 ^ 2e3 ^e4) = 0
        first = Multivector(bitmap=0b0001)
        
        second = Multivector(coef=2, bitmap=0b1101)
        
        self.assertEquals(self.zero, first ^ second)
        
    def test_ex2_b1(self):
        #e2 ^ (e1 ^ 2e3 ^e4) = 0
        first = Multivector(coef=1, bitmap=0b0010)
        
        second = Multivector(coef=2, bitmap=0b1101)
        
        self.assertEquals(Multivector(coef=-2, bitmap=0b1111), first ^ second)

if __name__ == '__main__':
    unittest.main()