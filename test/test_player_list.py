import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import yaml
from models.player_list import PlayerList, PLAYER_LIB_PATH
from models.player import Player


class TestPlayerList(unittest.TestCase):

    def setUp(self):
        self.player1_name = "John Doe"
        self.handicap = 15
        self.player1 = Player(self.player1_name, self.handicap)

        self.player2_name = "Jane Doe"
        self.player2 = Player(self.player2_name, self.handicap)

    @patch("os.listdir", return_value=["player1.yaml", "player2.yaml", "not_a_player.txt"])
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.load")
    def test_load_player_library(self, mock_yaml_load, mock_file, mock_listdir):
        mock_yaml_load.side_effect = [self.player1, self.player2]  # Simulate loading two valid Player objects
        player_list = PlayerList()
        
        self.assertEqual(len(player_list.player_list), 2)
        self.assertIn(self.player1_name, player_list.player_list)
        self.assertIn(self.player2_name, player_list.player_list)
        self.assertIsInstance(player_list.player_list[self.player1_name], Player)
        
        mock_listdir.assert_called_once_with(PLAYER_LIB_PATH)
        self.assertEqual(mock_file.call_count, 2)  # Ensure we tried to open two files

    @patch("os.listdir", return_value=["invalid.yaml"])
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.load", return_value={})
    def test_load_invalid_player_file(self, mock_yaml_load, mock_file, mock_listdir):
        with self.assertRaises(TypeError):
            PlayerList()
        
        mock_listdir.assert_called_once_with(PLAYER_LIB_PATH)
        mock_file.assert_called_once_with(os.path.join(PLAYER_LIB_PATH, "invalid.yaml"), 'r')

    @patch("models.player_list.PlayerList._load_player_library", return_value={})
    def test_refresh_player_list(self, mock_load_player_library):
        player_list = PlayerList()
        player_list.refresh_player_list()
        self.assertEqual(player_list.player_list, {})
        self.assertEqual(mock_load_player_library.call_count, 2)  # Once in __init__ and once in refresh_player_list


if __name__ == "__main__":
    unittest.main()