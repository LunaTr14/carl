from pathlib import Path
from os.path import exists
import csv
class CSV():
    __csv_path = ""
    __csv_file = None
    __headings = []
    def __does_file_exist(self) -> bool:
        if(exists(self.__csv_path)):
            return True
        return False

    def __create_csv_file(self) -> None:
        Path(self.__csv_path).touch()

    def __create_headings(self) -> None:
        self.__set_write_mode()
        csv_writer = csv.writer(self.__csv_file,lineterminator="\r")
        csv_writer.writerow(self.__headings)
        
    def __init__(self,file_name : str, headings : list) -> None:
        self.__csv_path= file_name
        self.__headings = headings
        if(not self.__does_file_exist()):
            self.__create_csv_file()
            self.__create_headings()
        self.__csv_file = open(self.__csv_path,mode="r")

    def __set_read_mode(self) -> None:
        self.__csv_file = open(self.__csv_path,mode="r")
    
    def __set_write_mode(self) -> None:
        self.__csv_file = open(self.__csv_path,mode="w")

    def __set_append_mode(self) -> None:
        self.__csv_file = open(self.__csv_path,mode="a")

    def __get_headings(self) -> list:
        self.__set_read_mode()
        return self.__csv_file.readline().removesuffix("\n").split(",")

    def search_entry(self, column_name : str, val : str) ->list:
        self.__set_read_mode()
        headings = self.__get_headings()
        if(column_name not in headings):
            return []
        col_index = headings.index(column_name)
        csv_reader = csv.reader(self.__csv_file)
        valid_entries = []
        for row in csv_reader:
           # print(row)
            if(row[col_index] == val):
                valid_entries.append(row)
        return valid_entries
    
    def read_csv(self) -> list:
        self.__set_read_mode()
        csv_reader = csv.reader(self.__csv_file)
        rows = []
        for row in csv_reader:
            rows.append(row)
        return rows
    
    def remove_duplicates(self, heading : str, value: str) ->None:
        data = self.read_csv()
        heading_index = self.__headings.index(heading)
        for row in data:
            if row[heading_index] == value:
                data.pop(data.index(row))
        self.__write_csv(data)

    def __write_csv(self, rows :list) -> None:
        self.__set_write_mode()
        writer = csv.writer(self.__csv_file)
        writer.writerows(rows)

    def append_record(self,rows : list) -> None:
        self.__set_append_mode()
        csv_writer = csv.writer(self.__csv_file,lineterminator="\r")
        csv_writer.writerows(rows)
    
    def test_append_record(self) -> None:
        new_data = ["Test1","Test2","3Test"]
        self.__csv_path = "test.csv"
        self.__create_csv_file()
        self.__set_append_mode()
        self.append_record(new_data)
        self.__set_read_mode()
        file_data = self.read_csv()
        assert new_data in file_data, "\nData was not appended Correctly\nExpected: {new_data}\nGot: {file_data}"
    
    def test_create_headings(self) -> None:
        self.__headings = ["123","abc","1a1"]
        self.__csv_path = "test.csv"
        self.__create_csv_file()
        self.__create_headings()
        file_headings = self.__get_headings()
        assert file_headings == self.__headings, f"\nError in Heading Creation\nExpected: {self.__headings}\nGot:{file_headings}"


    def test_search(self):
        self.__headings = ["123","abc","1a1"]
        test_rows = [["abc","def",["ghij"]],["a2bc","d3ef","g4hij"]]
        self.__csv_path = "test.csv"
        self.__create_csv_file()
        self.__create_headings()
        self.__set_append_mode()
        self.append_record(test_rows[0])
        self.append_record(test_rows[1])
        result = self.search_entry("abc","d3ef")
        assert test_rows[1] in result,f"\nError in Search\nExpected: {test_rows[1]}\nGot:{result}"