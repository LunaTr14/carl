#from csv_handler import CSV
from random import Random
from time import time_ns
from os.path import abspath
class User():
    discord_id = ""
    sus_amount = 0
    game_id = ""
    inventory_id= ""
    workdir = abspath("./")

    def create_user(self,discord_id : str):
        self.user_id = self.create_id("user_id")
        self.discord_id = discord_id
        self.inventory_id = self.create_id("inventory_id")
        self.game_id = self.create_id("game_id")
    
    def create_id(self,prefix : str) -> int:
        rand = Random()
        rand.seed = f"{prefix}: {time_ns()}"
        return rand.randrange(99999,999999)
    
    def export_row(self):
        return [
            self.discord_id,
            self.sus_amount,
            self.game_id,
            self.inventory_id
        ]
    
    def set_values_from_row(self, row:list):
        self.discord_id = row[0]
        self.sus_amount = row[1]
        self.game_id = row[2]
        self.inventory_id = row[3]