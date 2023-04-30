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
    
    def test_search(self):
        expected = [["Test3","Test4","4","5","6"]]
        self.csv_obj.write(expected)
        results = self.csv_obj.search("Test3")
        self.assertEqual(results,expected,"search: " + "❌")
        print("search: " + "✅")

    def test_append(self):
        expected = [["Test5","Test6","7","8","9"],["Test7","Test8","10","11","12"]]
        self.csv_obj.write([expected[0]])
        self.csv_obj.append([expected[1]])
        results = self.csv_obj.read()
        self.assertEqual(results,expected,"append: " + "❌")
        print("append: " + "✅")
    
    def test_clean_duplicates(self):
        expected = ["Test7","Test8","13","14","15"]
        self.csv_obj.write([])
        self.csv_obj.append([expected,expected,expected])
        self.csv_obj.clean_duplicates()
        results = self.csv_obj.read()
        self.assertEqual(results,[expected],"clean_duplicates: " + "❌")
        print("clean_duplicates: " + "✅")
    
    def test_clean_duplicates_by_id(self):
        expected = [["Test7","Test8","10","11","12"]]
        for n in range(10):
            expected[0][3] = expected[0][3] + str(n)
            self.csv_obj.append(expected)
        self.csv_obj.clean_duplicates_by_id(expected[0][0])
        result = self.csv_obj.read()
        self.assertEqual(len(result), 1 ,"clean_duplicates_by_id: " + "❌")
        print("clean_duplicates_by_id: " + "✅")
    
    def test_remove_entries_by_id(self):
        self.csv_obj.write([[]])
        temp_entry = ["Test123","0","a"]
        for n in range(5):
            self.csv_obj.append([temp_entry])
        self.csv_obj.remove_entries_by_id(temp_entry[0])
        result = self.csv_obj.read()
        print(result)
        self.assertTrue(result == [],"remove_entries_by_id: " + "❌")
        
        print("remove_entries_by_id: " + "✅")

if(__name__ =="__main__"):
    print("-----START CSV TEST-----")
    t = TestCSVHandler()
    t.test_remove_entries_by_id()
    print("-----END END TEST-----")