from .entity import CarlEntity
from .csv_handler import CSV
class Game(CarlEntity):
    __game_id = ""
    __wins = 0
    __loss = 0
    __score = 1000
    BASE_SCORE = 100

    def incriment_win(self) -> None:
        self.__wins = self.__wins + 1

    def incriment_loss(self) -> None:
        self.__loss = self.__loss + 1
    
    def update_score(self, did_win : bool, recipient_score : int) -> None:
        point_value = ((recipient_score + self.BASE_SCORE) / self.__score)
        if(did_win):
            self.__score = self.__score + point_value
        self.__score = self.__score - point_value
    
    def get_score(self) -> int:
        return self.__score
    
    def __init__(self,game_csv : CSV, game_id : str = "") -> None:
        if(not game_csv.does_entry_exist(game_id)):
            game_id = self.create_id("game")
        self.__game_id = game_id
    
    def save_game(self,csv_file:CSV) -> None:
        csv_file.remove_duplicates(self.__game_id)
        csv_file.append_row([self.__game_id,self.__wins,self.__loss,self.__score])