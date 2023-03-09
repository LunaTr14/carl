from json import load,dump
from pathlib import Path
from os.path import exists
import csv
from os.path import abspath

WORKDIR = abspath("./")
class JsonParser():
    _file_path = ""
    def __init__(self, path: str) -> None:
        self._file_path = path
        if(not exists(path)):
            self.create_empty_json()
        
    def read_content(self) -> dict:
        content_file = open(file=self._file_path, mode="r")
        data = load(content_file)
        content_file.close()
        return data
    
    def create_empty_json(self) -> None:
        Path(self._file_path).touch()
        self.write_content({})
    
    def write_content(self, data: dict) -> None:
        content_file = open(file=self._file_path, mode="w")
        dump(data, content_file)
        content_file.close()

    def _does_path_exist(self,path : str) -> bool:
        return exists(path)

class CSVFile():
    __csv_file = ""
    __headings = []
    def does_file_exist(self) -> bool:
        if(exists(self.__csv_file)):
            return True
        return False
    
    def create_csv_file(self) -> None:
        Path(self.__csv_file).touch()

    def create_headers(self) -> None:
        with open(self.__csv_file, mode="w") as f:
            csv_writer = csv.writer(f,lineterminator="\r")
            csv_writer.writerow(self.__headings)
        f.close()

    def __init__(self,file_name : str, headings : list) -> None:
        self.__csv_file= file_name
        self.__headings = headings
        if(not self.does_file_exist()):
            self.create_csv_file()
            self.create_headers()

    def search_entry(self, column_name : str, val : str) ->list:
        with open(self.__csv_file, mode="r") as f:
            headings = f.readline().split(",")
            csv_reader = csv.reader(f)
            row_number = -1
            valid_entries = []
            for index in range(len(headings)):
                if(headings[index] == column_name):
                    row_number = index
            if(row_number == -1):
                return ["Column does not Exist"]
            for row in csv_reader:
                if(row[row_number] == val):
                    valid_entries.append(row)
        
        return [valid_entries]
    
    def append_record(self,data : str) -> None:
        with open(self.__csv_file, mode="a") as f:
            csv_writer = csv.writer(f,lineterminator="\r")
            csv_writer.writerow(data)
    
                
class Item():
    item_id = ""
    name = ""
    booster = 0

class Inventory():
    inventory_id = ""
    items = {}

class GameDetails():
    game_id = ""
    wins = 0
    loss = 0
    score = 0

class User():
    user_id = ""
    discord_id = ""
    sus_amount = 0
    game_id = ""
    inventory_id= ""

    