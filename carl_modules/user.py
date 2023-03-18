from os.path import abspath
from .csv_handler import CSV
from random import randrange
from time import time_ns
class User():
    __discord_id = ""
    __sus_amount = 0
    __game_id = ""
    __user_csv = CSV

    def get_discord_id(self) -> str:
        return self.__discord_id

    def add_sus(self) -> None:
        self.__sus_amount = self.__sus_amount + 1
        self.__save_entry()
    
    def get_sus(self) -> int:
        return self.__sus_amount
    
    def get_game_id(self) -> str:
        return str(self.__game_id)

    def __create_id(self) -> str:
        return str(randrange(99999,999999) * time_ns())[0:6]
    def __save_entry(self):
        self.__user_csv.save([
            self.__discord_id,
            self.__sus_amount,
            self.__game_id
            ])
    
    def __init__(self,user_csv: CSV, game_csv: CSV,discord_id : str) -> None:
        self.__user_csv = user_csv
        for n in user_csv.search(discord_id):
            if(str(n[0]) == str(discord_id)):
                csv_entry = user_csv.search(discord_id)[0]
                self.__sus_amount = int(csv_entry[1])
                self.__game_id = csv_entry[2]
                self.__discord_id = discord_id
                return
        self.__discord_id = discord_id
        self.__game_id = self.__create_id()
        self.__save_entry()
        game_csv.save([self.__game_id,1000,1])