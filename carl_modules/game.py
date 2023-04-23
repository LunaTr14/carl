from csv_handler import CSV
from random import random

class Game():
    BASE_SCORE = 100
    __game_csv = CSV
    

    def __init__(self) -> None:
        self.__game_csv = CSV("game.csv","./")
    
    def find_user(self, user_id : str) -> list:
        return self.__game_csv.search(user_id)[0]
    
    def calculate_score(self,winner_points : int,loser_points : int) -> list:
        point_change = abs(winner_points - loser_points) * 0.6
        if(winner_points > loser_points):
            point_change = abs(winner_points - loser_points) * 0.3
        result = [int(winner_points + point_change), int(loser_points - point_change)]
        return result
    
    def update_entry(self,update_entry : list) -> None:
        data = self.__game_csv.read()
        new_data = []
        for n in data:
            if(n[0] != update_entry[0]):
                new_data.append(n)
        new_data.append(update_entry)
        self.__game_csv.write(new_data)
        self.__game_csv.clean_duplicates_by_id(update_entry[0])
    
    def does_user_exist(self, user_id : str) -> bool:
        if(len(self.__game_csv.search(user_id)) > 0):
            return True 
        return False
    
    def add_user(self,user_details : list) -> None:
        self.__game_csv.append([user_details])
    
    def clear_csv(self) -> None:
        self.__game_csv.write([])