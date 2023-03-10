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
    
    def get_sus(self) -> int:
        return self.__sus_amount
    
    def get_inventory_id(self) -> str:
        return self.__inventory_id
    def get_game_id(self) -> str:
        return self.__game_id
    
    def get_discord_id(self) -> str:
        return self.__discord_id

    def increment_sus(self) -> None:
        self.__sus_amount = self.__sus_amount + 1

    def get_inventory(self,inventory_csv : CSV) -> Inventory:
        inventory_row = inventory_csv.get_entry("inventory_id",self.__inventory_id)
        inv = Inventory()
        inv.set_values_from_row(inventory_row)
        return inv
    
    def get_game(self,game_csv : CSV) -> Game:
        game_row = game_csv.get_entry("game_id",self.__game_id)
        game = Game()
        game.set_values_from_row(game_row)
        return game

    def save_user(self,user_csv:CSV) -> None:
        user_csv.remove_duplicates(self.__discord_id)
        user_csv.append_row([self.__discord_id,self.__sus_amount,self.__game_id,self.__inventory_id])

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