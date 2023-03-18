from carl_modules.csv_handler import CSV
from random import random

class Game():
    BASE_SCORE = 100
    __game_csv = CSV
    
    #Calculates the Chances of winning for the User in Current Object
    def __calculate_win_chance(self,sender_boost,opponent_boost : int) -> float:
        return int(sender_boost) / (int(sender_boost) + int(opponent_boost))
    
    def __determine_winner(self, win_chance : float) -> str:
        rand = random()
        if (win_chance > rand):
            return "SENDER"
        return "OPPONENT"

    def __init__(self,game_csv :CSV) -> None:
        self.__game_csv = game_csv

    def fight(self, sender_row : list,opponent_row : list) -> str:
        if(int(sender_row[1]) <= 0 or int(opponent_row[1]) <= 0):
            return "Insufficient Points"
        win_chance = self.__calculate_win_chance(sender_row[2],opponent_row[2])
        winner = self.__determine_winner(float(win_chance))
        if(winner == "SENDER"):
            sender_row[1] = str(int(sender_row[1]) + self.BASE_SCORE)
            opponent_row[1] = str(int(opponent_row[1]) - self.BASE_SCORE)
        else:
            sender_row[1] = str(int(sender_row[1]) - self.BASE_SCORE)
            opponent_row[1] = str(int(opponent_row[1]) + self.BASE_SCORE)
        self.__game_csv.save(sender_row)
        self.__game_csv.save(opponent_row)
        return winner