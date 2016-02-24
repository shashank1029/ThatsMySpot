'''


@author: shashank
'''
import unittest

from datatbase.dbFunctions import dbFunctions
from datatbase.esFunctions import esFunctions


class searchTest(unittest.TestCase):


    def testGetSpots(self):
        '''name of test starts with test to be considered in unit testing'''
        es = esFunctions()
        #db = dbFunctions()
        print(es.getAvailableSpots(40.7410986, -73.9888682, 1))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()