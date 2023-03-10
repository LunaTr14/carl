from random import Random
from time import time_ns
from .csv_handler import CSV
class CarlEntity():
    def create_id(self,prefix : str) -> str:
        rand = Random()
        rand.seed = f"{prefix}: {time_ns()}"
        return str(rand.randrange(99999,999999))
    
    def create(self) -> None:
        pass

    def export_row(self) -> list:
        return [] 
    
    def set_values_from_row(self, row:list) -> None:
        pass

    def create_if_empty(self, csv_obj : CSV,search_heading : str, search_value : str) -> None:
        if(csv_obj.does_entry_exist(search_heading,search_value)):
            self.set_values_from_row([csv_obj.get_entry(search_heading,search_value)])
        else:
            self.create()