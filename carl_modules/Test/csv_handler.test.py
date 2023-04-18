import unittest
import sys
from os.path import abspath
sys.path.append("../")
from csv_handler import CSV



class TestCSVHandler(unittest.TestCase):
    TEST_PATH = abspath("./Test/.temp_test/")
    TEST_FILE = "test.file"
    csv_obj = CSV(TEST_PATH, TEST_FILE)
    
    
    def testReadWrite(self):
        expected = [["Test1","Test2","1","2","3"]]
        self.csv_obj.write(expected[0])
        result = self.csv_obj.read()
        self.assertEqual(result,expected,"\nreadWrite: " + u'\u274C')
        print("\nreadWrite: " + u'\u2713')
    
    def testSearch(self):
        expected = [["Test3","Test4","4","5","6"]]
        self.csv_obj.write(expected[0])
        results = self.csv_obj.search("Test3")
        self.assertEqual(results,expected,"\nsearch: " + u'\u274C')
        print("\nappend: " + u'\u2713')

    def testAppend(self):
        expected = [["Test5","Test6","7","8","9"],["Test7","Test8","10","11","12"]]
        self.csv_obj.write(expected[0])
        self.csv_obj.append(expected[1])
        results = self.csv_obj.read()
        self.assertEqual(results,expected,"append: " + u'\u274C')
        
    
    def testCleanDuplicates(self):
        expected = ["Test7","Test8","13","14","15"]
        for i in range(3):
            self.csv_obj.append(expected)
        self.csv_obj.cleanDuplicates(expected[0])
        results = self.csv_obj.read()
        self.assertEqual(results,expected,"cleanDuplicates: " + u'\u274C')

if(__name__ =="__main__"):
    print("\n-----START CSV TEST-----\n")
    unittest.main()
    print("-----END END TEST-----")