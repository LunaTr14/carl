from pathlib import Path
from os.path import exists, abspath
from os import mkdir, rmdir
from random import randrange
import csv
class CSV():
    _csv_file = None
    _csv_path = ""
    def does_entry_exist(self, value : str) -> bool:
        if(self.get_entry(value) == []):
            return False
        return True
        
    def __get_folder_tree(self, path: str) -> list:
        return path.split("/")
    
    def _create_missing_folders(self,folder_path: str) -> None:
        dir_tree = self.__get_folder_tree(folder_path)
        full_path = ""
        for folder in dir_tree:
            full_path = full_path + "/"+folder
            if(not exists(full_path)):
                mkdir(abspath(full_path))
        
    def __init__(self,csv_path : str) -> None:
        self._csv_path = csv_path

    def _set_mode(self, mode : str) -> None:
        self._csv_file.close()
        self._csv_file = open(self._csv_path,mode=mode)

    def get_entry(self, search_item : str) ->list:
        data = self.read_csv()
        valid_entries = []
        for row in data:
            if(search_item in row):
                valid_entries.append(row)
        return valid_entries
    
    def read_csv(self) -> list:
        self._set_mode("r")
        csv_reader = csv.reader(self._csv_file)
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
        self._set_write_mode()
        csv_writer = csv.writer(self._csv_file,lineterminator="\r")
        csv_writer.writerows(data)

    def append_row(self, row :list) ->None:
        self._set_mode("a")
        csv_appender = csv.writer(self._csv_file,lineterminator="\r")
        csv_appender.writerow(row)
    
class CSVTest(CSV):
    __workdir = abspath("./test")
    def __init__(self) -> None:
        super().__init__(self.__workdir+"/temp.csv")
    
    def __create_testing_files(self,path : str,file_name : str):
        self._create_missing_folders(path)
        self._csv_file = open(path+"/"+file_name,mode="w")

    def __create_random_path(self) -> str:
        return self.__workdir + "/" + str(randrange(0,99999))
    
    def test_folder_create(self):
        folder_path = self.__create_random_path()
        self._create_missing_folders(folder_path)
        assert exists(folder_path), f"\nMissing Folder\nLocation: {folder_path}"
        print(f"Folder Created Result: {folder_path}")
    
    def test_set_mode(self):
        self.__create_testing_files(self.__create_random_path(),"test.tmp")
        for mode in ["r","w","a"]:
            self._set_mode(mode)
            assert self._csv_file.mode == mode, f"Mode Error Expected {mode}\nGot: {self._csv_file.mode}"
        print("File mode Switching Working")

    def test_append_record(self):
        self.__create_testing_files(self.__create_random_path(),"test.tmp")
        test_list = ["0123","asvsd","dsfdsf","qwewqe"]
        self.append_row(test_list)
        result = self.read_csv()
        assert self.read_csv() == [test_list], f"\nError in appending / reading file\nFile Path: {self._csv_path}\nExpected {test_list}\nGot: {[result]}"
        print("Append / Read Working")
    
    def test_all(self):
        self.test_folder_create()
        self.test_set_mode()
        self.test_append_record()