import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import yaml
from models.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player_name = "John Doe"
        self.handicap = 15
        self.player = Player(self.player_name, self.handicap)

    def test_initialization(self):
        self.assertEqual(self.player.name, self.player_name)
        self.assertEqual(self.player.twisted_creek_handicap, self.handicap)
        self.assertEqual(self.player.mosley_open_handicap, min(20, self.handicap))
        self.assertFalse(self.player.active)
        self.assertEqual(self.player.save_path, os.path.abspath(f'playerlib/{self.player_name}.yaml'))

    def test_validate_name(self):
        with self.assertRaises(TypeError):
            Player(123, self.handicap)

        with self.assertRaises(ValueError):
            Player("", self.handicap)

    def test_validate_handicap(self):
        with self.assertRaises(TypeError):
            Player(self.player_name, "not a number")

        with self.assertRaises(ValueError):
            Player(self.player_name, -1)

        with self.assertRaises(ValueError):
            Player(self.player_name, 31)

    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    def test_save(self, mock_yaml_dump, mock_file):
        self.player.save()
        mock_file.assert_called_once_with(self.player.save_path, 'w')
        mock_yaml_dump.assert_called_once_with(self.player, mock_file())

    @patch("models.player.path.exists", return_value=True)
    @patch("models.player.remove")
    def test_delete(self, mock_remove, mock_path_exists):
        self.player.delete()
        mock_path_exists.assert_called_once_with(self.player.save_path)
        mock_remove.assert_called_once_with(self.player.save_path)

    @patch("models.player.remove", side_effect=Exception("Some error"))
    @patch("models.player.path.exists", return_value=True)
    def test_delete_exception(self, mock_path_exists, mock_remove):
        with self.assertRaises(IOError):
            self.player.delete()
        mock_path_exists.assert_called_once_with(self.player.save_path)
        mock_remove.assert_called_once_with(self.player.save_path)


if __name__ == "__main__":
    unittest.main()