from carl_modules.csv_handler import CSV
from random import random

class Game():
    BASE_SCORE = 100
    __game_csv = CSV
    
    #Calculates the Chances of winning for the User in Current Object
    def __calculate_win_chance(self,sender_boost,opponent_boost : int) -> float:
        return int(sender_boost) / (int(sender_boost) + int(opponent_boost))
    
    def __is_winner_sender(self, win_chance : float) -> bool:
        rand = random()
        if (win_chance > rand):
            return True
        return False

    def __init__(self,game_csv :CSV) -> None:
        self.__game_csv = game_csv

    def __calculate_score(self,winner :int, loser :int) -> tuple:
        if(winner > loser):
            adjustment_score = round(0.75 * (winner - loser))
            winner = winner + adjustment_score
            loser = loser - adjustment_score
        elif(winner < loser):
            adjustment_score = round(1.25 * (loser - winner))
            winner = winner + adjustment_score
            loser = loser + adjustment_score
        winner = winner + 100
        loser = loser - 100
        return (winner,loser)

    def fight(self, sender_row : list,opponent_row : list) -> str:
        sender_points = round(float(sender_row[1]))
        opponent_points = round(float(opponent_row[1]))
        if(sender_points <= 0 or opponent_points <= 0):
            return "Insufficient Points"
        
        sender_boost = round(float(sender_row[2]))
        opponent_boost = round(float(sender_row[2]))
        win_chance = self.__calculate_win_chance(sender_boost,opponent_boost)
        is_winner_sender = self.__is_winner_sender(float(win_chance))
        
        if(is_winner_sender ):
            new_score_tuple = self.__calculate_score(sender_points,opponent_points)
            sender_row[1] = str(new_score_tuple[0])
            opponent_row[1] = str(new_score_tuple[1])
            winner_details = sender_row
        elif(not is_winner_sender):
            new_score_tuple = self.__calculate_score(opponent_points,sender_points)
            opponent_row[1] = str(new_score_tuple[0])
            sender_row[1] = str(new_score_tuple[1])
            winner_details = opponent_row
        
        self.__game_csv.save(sender_row)
        self.__game_csv.save(opponent_row)
        return winner_details