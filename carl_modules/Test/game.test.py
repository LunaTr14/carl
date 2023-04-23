import unittest
import sys
from os.path import abspath
sys.path.append("../")
from game import Game
class TestGame(unittest.TestCase):
    _game = Game

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._game = Game()
    
    def test_find_user(self):
        sample_entry = ["++sample_id++","points","win_chance","wins","losses"]
        self._game.clear_csv()
        self._game.add_user(sample_entry)
        result = self._game.find_user(sample_entry[0])
        self.assertEqual(sample_entry,result,"\nfind_user: " + "❌")
        print("\nfind_user: " + "✅")
    
    def test_calculate_score(self):
        expected_points = [80,70]
        winner_points = 50
        loser_points = 100
        result = self._game.calculate_score(winner_points,loser_points)
        self.assertEqual(expected_points,result,"\ncalculate_points: " + "❌")
        expected_points = [115,35]
        loser_points = 50
        winner_points = 100
        result = self._game.calculate_score(winner_points,loser_points)
        self.assertEqual(expected_points,result,"\ncalculate_points: " + "❌")
        print("\ncalculate_points: " + "✅")
    
    def test_does_user_exist(self):
        sample_entry = ["++sample_id++",102,23,1,2]
        self._game.clear_csv()
        result = self._game.does_user_exist(sample_entry[0])
        self.assertFalse(result,"\nError: User does not exist, " + "❌")
        self._game.update_entry(sample_entry)
        result = self._game.does_user_exist(sample_entry[0])
        self.assertTrue(result,"\nError: User exists, " + "❌")
        print("\ndoes_user_exist: " + "✅")

if __name__ == "__main__":
    unittest.main()