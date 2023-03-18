from .csv_handler import CSV
from random import random, randrange
from time import time_ns

class Game():
    __game_id = ""
    __score = 1000
    __boost = 1
    BASE_SCORE = 100
    __game_csv = CSV


    def __get_opponent(self, opponent_id: str) -> list:
        for entry in self.__game_csv.search(opponent_id):
            print(entry)
            if(entry[0] == opponent_id):
                return entry

    def get_score(self) -> int:
        return self.__score
    
    #Calculates the Chances of winning for the User in Current Object
    def __calculate_win_chance(self,opponent_boost : int) -> float:
        return int(self.__boost) / (int(self.__boost) + int(opponent_boost))
    
    def __determine_winner(self, win_chance : float) -> str:
        rand = random()
        if (win_chance > rand):
            return "SENDER"
        return "OPPONENT"
    
    def __create_id(self) -> str:
        return str(randrange(99999,999999) * time_ns())[0:6]

    def __init__(self,game_csv : CSV, game_id : str) -> None:
        self.__game_csv = game_csv
        user = self.__game_csv.search(game_id)
        if(user == []):
            self.__game_id = self.__create_id()
            self.save_game()
        else:
            self.__game_id = game_id
            self.__score = int(user[0][1])
            self.__boost = int(user[0][2])


    def save_game(self) -> None:
        self.__game_csv.append_row([self.__game_id,self.__score,self.__boost])

    def fight(self, opponent_id : str) -> str:
        opponent_entry = self.__get_opponent(opponent_id)
        win_chance = self.__calculate_win_chance(opponent_entry[2])
        winner = self.__determine_winner(float(win_chance))
        if(winner == "SENDER"):
            self.__score = self.__score + self.BASE_SCORE
            opponent_entry[1] = str(int(opponent_entry[1]) - self.BASE_SCORE)
        else:
            print(opponent_entry)
            opponent_entry[1] = str(int(opponent_entry[1]) + self.BASE_SCORE)
            self.__score = self.__score - self.BASE_SCORE
        self.save_game()
        self.__game_csv.append_row(opponent_entry)
        return winner