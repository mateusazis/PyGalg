# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:25:52 2013

@author: mateus
"""
import sys
sys.path.append("../src")

from Multivector import Multivector
from Multivector import _canonical_reordering
import unittest

class MultivectorTests(unittest.TestCase):
       
    def test_ex1_a(self):
        first = Multivector({0b1 : 1, 0b10 : 1})      
        second = Multivector({0b100 : 1, 0b10 : 1})
        op = first ^ second
        
        expected = Multivector({0b11 : 1, 0b110 : 1, 0b101 : 1})
        self.assertEqual(expected, op)  
       
    def test_ex1_b(self):
        first = Multivector([0, -1, 1])        
        second = Multivector([0, 1, 0, 0, -2])
        op = first ^ second
        
        expected = Multivector({0b011:-1, 0b110:-2, 0b101:2})
        self.assertEqual(expected, op)
        
    def test_ex1_c(self):
        first = Multivector([0, 4, 1, 0, 1])      
        second = Multivector([0, 3])
        op = first ^ second
        
        expected = Multivector({0b11 : -3, 0b101 : -3})
        self.assertEqual(expected, op)
        
    def test_ex1_d(self):
        first = Multivector({0b10 : 1, 0b100 : 1})      
        second = Multivector({0b1 : 0.5, 0b10 : 1, 0b100 : 1.5})
        op = first ^ second
        
        expected = Multivector({0b11 : -0.5, 0b110 : 0.5, 0b101 : -0.5})
        self.assertEqual(expected, op)
    
    def test_reorder(self):
        sign = _canonical_reordering(0b100, 0b001)
        expected = -1
        self.assertEqual(expected, sign)
    
if __name__ == '__main__':
    unittest.main()