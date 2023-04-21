from os.path import exists, abspath
from os import makedirs
import csv
class CSV():
    _csv_path = ""

    def __init__(self,file_name : str, file_path : str) -> None:
        full_path = file_path + "/" + file_name
        if(not exists(file_path)):
            makedirs(file_path)
        if(not exists(full_path)):
            open(full_path,mode="w").close()
        self._csv_path = full_path

    def read(self) -> list:
        data = []
        with open(self._csv_path,mode="r",encoding="ASCII") as csv_file:
            reader = csv.reader(csv_file,lineterminator="\n")
            for row in reader:
                data.append(row)
            csv_file.close()
        return data

    def write(self, rows : list):
        with open(self._csv_path, mode="w",encoding="ASCII") as csv_file:
            writer = csv.writer(csv_file,lineterminator="\n")
            writer.writerows(rows)
            csv_file.close()

    def append(self, rows : list) -> None:
        with open(self._csv_path, mode="a") as csv_file:
            writer = csv.writer(csv_file,lineterminator="\n")
            writer.writerows(rows)
            csv_file.close()
   
    def search(self, query : str) -> list:
        results = []
        data = self.read()
        for row in data:
            if(query not in results):
                results.append(row)
        return results

    def clean_duplicates(self) -> None:
        data = self.read()
        results = []
        for row in data:
            if(row not in results):
                results.append(row)
        
        self.write(results)