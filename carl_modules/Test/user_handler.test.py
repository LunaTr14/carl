import unittest
import sys
from os.path import abspath
sys.path.append("../")
from user_handler import UserHandler
from csv_handler import CSV
class TestGame(unittest.TestCase):
    _user_handler = UserHandler
    
    
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        csv = CSV("temp.game.test","./Test/")
        self._user_handler = UserHandler(csv)
    
    def __clear_csv(self) -> None:
        self._user_handler.csv.write([[]])

    def test_add_user(self):
        self.__clear_csv()
        self._user_handler.add_user(["idtest123","444"])
        data = self._user_handler.find_user("idtest123")
        self.assertEqual(["idtest123","444"],data)

    def update_user(self):
        self.__clear_csv()
        self._user_handler.add_user(["idtest123","444"])
        self._user_handler.update_user("idtest",["idtest123","4s44"])
        data = self._user_handler.find_user("idtest123")
        self.assertEqual(data,["idtest123","4s44"])
    
if __name__ == "__main__":
    unittest.main()