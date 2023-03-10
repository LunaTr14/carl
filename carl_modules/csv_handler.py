from pathlib import Path
from os.path import exists
import csv
class CSV():
    __csv_path = ""
    __csv_file = None
    __headings = []
    def does_entry_exist(self, value : str) -> bool:
        if(self.get_entry(value) == []):
            return False
        return True
        
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

    def get_entry(self, search_item : str) ->list:
        data = self.read_csv()
        valid_entries = []
        for row in data:
            if(search_item in row):
                valid_entries.append(row)
        return valid_entries
    
    def read_csv(self) -> list:
        self.__set_read_mode()
        csv_reader = csv.reader(self.__csv_file)
        rows = []
        for row in csv_reader:
            rows.append(row)
        return rows
    
    def remove_duplicates(self, id : str) -> None:
        data = self.read_csv()
        for row in data:
            for entry in row:
                if entry == id:
                    data.pop(data.index(row))
                    break
        self.__set_write_mode()
        csv_writer = csv.writer(self.__csv_file,lineterminator="\r")
        csv_writer.writerows(data)

    def append_row(self, row :list) ->None:
        self.__set_append_mode()
        csv_appender = csv.writer(self.__csv_file,lineterminator="\r")
        csv_appender.writerow(row)