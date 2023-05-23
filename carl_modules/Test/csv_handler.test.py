import unittest
import sys
from os.path import abspath
sys.path.append("../")
from csv_handler import CSV

class TestCSVHandler(unittest.TestCase):
    TEST_PATH = abspath("./Test/.temp_test/")
    TEST_FILE = "test.file"
    csv_obj = CSV(TEST_FILE,TEST_PATH)
    
    def test_read_write(self):
        expected = [["Test1","Test2","1","2","3"],["Test1a","Testb2","cc1","aa2","a3"]]
        self.csv_obj.write(expected)
        result = self.csv_obj.read()
        self.assertEqual(result,expected," read_write: " + "❌")
        print("read_write: " + "✅")

    def test_append(self):
        expected = [["Test5","Test6","7","8","9"],["Test7","Test8","10","11","12"]]
        self.csv_obj.write([expected[0]])
        self.csv_obj.append([expected[1]])
        results = self.csv_obj.read()
        self.assertEqual(results,expected,"append: " + "❌")
        print("append: " + "✅")

if(__name__ =="__main__"):
    print("-----START CSV TEST-----")
    unittest.main()
    print("-----END END TEST-----")