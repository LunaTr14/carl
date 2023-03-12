from os.path import exists, abspath
from os import mkdir
from random import randrange
import csv
class CSV():
    _csv_file = None
    _csv_path = ""
        
    def __get_folder_tree(self, path: str) -> list:
        return path.split("/")
    
    def __create_file(self):
        open(self._csv_path,mode="w").close()

    def __create_missing_files(self) -> None:
        dir_tree = self.__get_folder_tree(self._csv_path)
        full_path = ""
        for folder in dir_tree:
            full_path = full_path + "/"+folder
            if(not exists(full_path) and "." not in full_path):
                mkdir(abspath(full_path))
        self.__create_file()
    
    def __init__(self,csv_path : str) -> None:
        self._csv_path = csv_path
        if(not exists(self._csv_path)):
            self.__create_missing_files()
        self._csv_file = open(csv_path,mode='r') 

    def __set_mode(self, mode : str) -> None:
        self._csv_file.close()
        self._csv_file = open(self._csv_path,mode=mode)
    
    def __remove_duplicates(self, id : str) -> None:
        data = self.__read_csv()
        for row in data:
            for entry in range(len(row)):
                if(row[entry][0] == id):
                    data.pop(entry)
        self.__set_mode("w")
        csv_writer = csv.writer(self._csv_file,lineterminator="\r")
        csv_writer.writerows(data)

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
            if(search_item in row):
                valid_entries.append(row)
        return valid_entries
    
    def append_row(self, row :list) ->None:
        self.__set_mode("a")
        csv_appender = csv.writer(self._csv_file,lineterminator="\r")
        csv_appender.writerow(row)

    def save(self, data : list) -> None:
        self.__remove_duplicates(data[0])
        self.append_row(data)

class CSVTest(CSV):
    __workdir = abspath("./test")
    def __init__(self) -> None:
        self.__create_random_path()
        super().__init__(self.__workdir+"/temp.csv")

    def __create_random_path(self) -> None:
        self.__workdir =  self.__workdir + "/" + str(randrange(0,99999))
    
    def test_folder_create(self):
        assert exists(self._csv_path), f"\nMissing Folder\nLocation: {self._csv_path}"
        print(f"Folder Created Result: {self._csv_path}")

    def test_append_record(self):
        test_list = ["0123","asvsd","dsfdsf","qwewqe"]
        self.append_row(test_list)
        result = self.search(test_list[0])
        assert result == [test_list], f"\nError in appending / reading file\nFile Path: {self._csv_path}\nExpected {test_list}\nGot: {[result]}"
        print("Append / Read Working")
    
    def test_all(self):
        self.test_folder_create()
        self.test_append_record()