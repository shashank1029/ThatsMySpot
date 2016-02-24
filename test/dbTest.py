'''
Created on 24 Feb 2016

@author: osboxes
'''
import unittest
from datatbase.dbFunctions import dbFunctions


class dbTest(unittest.TestCase):


    def ltestParkUser(self):
        db = dbFunctions()
        db.parkUser('TEST',40.987654, -70.1234567, 1)
        
    def testReleaseSpotUser(self):
        db = dbFunctions()
        db.emptySpace('TEST', 1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #import sys;sys.argv = ['', 'Test.parkUserTest']
    unittest.main()