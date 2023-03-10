from .entity import CarlEntity
from .csv_handler import CSV
class Item(CarlEntity,CSV):
    __item_id = ""
    __name = ""
    __boost = 0

    def __init__(self,item_csv: CSV, item_id :str = "") -> None:
        if(not item_csv.does_entry_exist("item_id",item_id)):
            self.__item_id = self.create_id("item")
            self.__name = ""
            self.__boost = 0
        else:
            item_entry = item_csv.get_entry(item_id)
            self.__name = item_entry[1]
            self.__boost = item_entry[2]

    def set_name(self,name : str) ->None:
        self.__name = name

    def set_booster(self,boost : int) -> None:
        self.__boost = boost
    
    def get_boost(self) -> int:
        return self.__boost
    def get_name(self) -> str:
        return self.__name
    def export_row(self) -> None:
        return [
            self.__item_id,
            self.__name,
            self.__boost
        ]
    