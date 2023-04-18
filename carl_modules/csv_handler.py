from os.path import exists, abspath
from os import mkdir
from random import randrange
import csv
class CSV():
    _csv_file = None
    _csv_path = ""
        
    def __get_folder_tree(self, path: str) -> list:
        return path.split("/")

    def __create_missing_files(self) -> None:
        dir_tree = self.__get_folder_tree(self._csv_path)
        full_path = ""
        for folder in dir_tree:
            full_path = full_path + "/"+folder
            if(not exists(full_path) and "." not in full_path):
                mkdir(abspath(full_path))
        open(self._csv_path,mode="w").close()
    
    def __init__(self,csv_path : str) -> None:
        self._csv_path = csv_path
        if(not exists(self._csv_path)):
            self.__create_missing_files()
        self._csv_file = open(csv_path,mode='r') 

    def __set_mode(self, mode : str) -> None:
        self._csv_file.close()
        self._csv_file = open(self._csv_path,mode=mode)
    
    def __remove_duplicates(self, id : str) -> None:
        valid_entries = []
        for row in self.__read_csv():
            if(row[0] != id):
                valid_entries.append(row)
        self.__set_mode("w")
        self._csv_file.write("")
        csv_writer = csv.writer(self._csv_file,lineterminator="\r")
        csv_writer.writerows(valid_entries)

    def __read_csv(self) -> list:
        self.__set_mode("r")
        csv_reader = csv.reader(self._csv_file)
        rows = []
        for row in csv_reader:
            rows.append(row)
        return rows

    def search(self, search_item : str) ->list:
        data = self.__read_csv()
        valid_entries = []
        for row in data:
            for cell in row:
                if(search_item == cell):
                    valid_entries.append(row)
        return valid_entries

    def does_entry_exist(self, id : str) -> bool:
        for n in self.__read_csv():
            if(str(n[0]) == id):
                return True
        return False

    def save(self, data : list) -> None:
        self.__remove_duplicates(data[0])
        self.__set_mode("a")
        csv_writer = csv.writer(self._csv_file,lineterminator="\r")
        csv_writer.writerow(data)