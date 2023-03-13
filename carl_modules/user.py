from .entity import CarlEntity
from os.path import abspath
from .csv_handler import CSV
from .inventory import Inventory
from .game import Game
class User(CarlEntity):
    __discord_id = ""
    __sus_amount = 0
    __game_id = ""
    __inventory_id= ""
    __user_csv = CSV
    __inventory_csv = CSV

    def get_discord_id(self) -> str:
        return self.__discord_id

    def add_sus(self) -> None:
        self.__sus_amount = self.__sus_amount + 1
    
    def save_entry(self):
        self.__user_csv.save([
            self.__discord_id,
            self.__sus_amount,
            self.__game_id,
            self.__inventory_id
            ])
    
    def __init__(self,user_csv: CSV, discord_id: str = "") -> None:
        self.__discord_id = discord_id
        if(not user_csv.does_entry_exist(discord_id)):
            self.__inventory_id = self.create_id("inventory")
            self.__game_id = self.create_id("game")
        else:
            csv_entry = user_csv.get_entry(discord_id)[0]
            self.__discord_id = discord_id
            self.__sus_amount = csv_entry[1]
            self.__game_id = csv_entry[2]
            self.__inventory_id = csv_entry[3]