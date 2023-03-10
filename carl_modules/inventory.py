from .entity import CarlEntity
from .item import Item
from .csv_handler import CSV
class Inventory(CarlEntity,CSV):
    __inventory_id = ""
    __items = {}

    def __init__(self,inventory_id : str ="") -> None:
        if(inventory_id == ""):
            inventory_id = self.create_id("inventory")
        self.__inventory_id = inventory_id
    
    def export_row(self) -> list:
        return [self.__inventory_id,self.__items]
    
    def add_item(self,item_id : int, amount : int) -> None:
        if(item_id not in self.__items.keys):
            self.__items[item_id] = 0
        self.__items[item_id] = self.__items[item_id] + amount

    def get_items(self) -> dict:
        return self.__items
    
    def save(self,csv_inventory: CSV) ->None:
        csv_inventory.remove_duplicates(self.__inventory_id)
        csv_inventory.append_row([self.__inventory_id,self.__items])

    def get_total_boost(self,csv_item :CSV) -> int:
        if(csv_item in self.__items.keys()):
            return int(self.__items[csv_item]["boost"])
        return -1