from .entity import CarlEntity
from .csv_handler import CSV
class Item(CarlEntity,CSV):
    __item_csv = CSV

    def __init__(self,item_csv: CSV) -> None:
        self.__item_csv = item_csv
    
    def __find_item(self,item_id) -> list:
        for entry in self.__item_csv.search(item_id):
            if(entry[0] == item_id):
                return entry
            
    def get_item_name(self,item_id : str) -> str:
        return self.__find_item(item_id)[1]
    def get_boost(self,item_id : str) -> int:
        return self.__find_item(item_id)[2]
