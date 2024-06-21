import unittest
from unittest.mock import patch, MagicMock
from controllers.player_list_controller import PlayerListController
from models.player import Player
import tkinter as tk

class TestPlayerListController(unittest.TestCase):

    def setUp(self):
        self.mock_app = MagicMock()
        self.mock_model = MagicMock()
        self.mock_view = MagicMock()

        # Initialize the PlayerListController with mocks
        self.controller = PlayerListController(self.mock_app, self.mock_model, self.mock_view)

    @patch('controllers.player_list_controller.MenuView')
    def test_open_menu(self, MockMenuView):
        self.controller.open_menu()
        self.mock_app.show_frame.assert_called_with(MockMenuView)

    def test_populate_player_data(self):
        player1 = MagicMock(spec=Player)
        player1.name = 'Player1'
        player1.mosley_open_handicap = 10
        player1.twisted_creek_handicap = 15
        player1.active = False

        player2 = MagicMock(spec=Player)
        player2.name = 'Player2'
        player2.mosley_open_handicap = 20
        player2.twisted_creek_handicap = 25
        player2.active = True

        self.mock_model.player_list = {
            'Player1': player1,
            'Player2': player2
        }

        self.mock_view.player_frames = {
            'Player1': MagicMock(),
            'Player2': MagicMock()
        }

        self.controller.populate_player_data()

        self.mock_view.player_frames['Player1'].player.config.assert_called_with(text='Player1')
        self.mock_view.player_frames['Player1'].mosley_open_hc.config.assert_called_with(text=10)
        self.mock_view.player_frames['Player1'].twisted_creek_hc.config.assert_called_with(text=15)
        self.mock_view.player_frames['Player1'].active_state.set.assert_called_with(value=False)

        self.mock_view.player_frames['Player2'].player.config.assert_called_with(text='Player2')
        self.mock_view.player_frames['Player2'].mosley_open_hc.config.assert_called_with(text=20)
        self.mock_view.player_frames['Player2'].twisted_creek_hc.config.assert_called_with(text=25)
        self.mock_view.player_frames['Player2'].active_state.set.assert_called_with(value=True)

    def test_get_player(self):
        player = MagicMock(spec=Player)
        player.name = 'Player1'
        self.mock_model.player_list = {'Player1': player}

        result = self.controller.get_player('Player1')
        self.assertEqual(result, player)

    def test_get_player_names(self):
        self.mock_model.player_list = {
            'Player1': MagicMock(spec=Player),
            'Player2': MagicMock(spec=Player)
        }

        result = self.controller.get_player_names()
        self.assertEqual(result, ['Player1', 'Player2'])

    @patch('models.player.Player.save')
    @patch('controllers.player_list_controller.PlayerListController.update_player_list')
    def test_activate_player(self, mock_save, mock_update_player_list):
        player = MagicMock(spec=Player)
        self.mock_model.player_list = {'Player1': player}

        self.controller.activate_player('Player1', True)
        self.assertTrue(player.active)
        self.assertTrue(player.save.called)
        mock_update_player_list.assert_called()

    def test_validate_handicaps(self):
        result = self.controller.validate_handicaps('10', '15')
        self.assertEqual(result, (10, 15))

        with self.assertRaises(ValueError):
            self.controller.validate_handicaps('', '15')

        with self.assertRaises(ValueError):
            self.controller.validate_handicaps('10', '')

        with self.assertRaises(TypeError):
            self.controller.validate_handicaps('abc', '15')

    @patch('models.player.Player.save')
    @patch('controllers.player_list_controller.Player')
    @patch('controllers.player_list_controller.PlayerListController.update_player_list')
    def test_update_player(self, MockPlayer, mock_save, mock_update_player_list):
        self.mock_view.player_entry_frame.player.get.return_value = 'Player1'
        self.mock_view.player_entry_frame.mosley_open_hc.get.return_value = '10'
        self.mock_view.player_entry_frame.twisted_creek_hc.get.return_value = '15'

        # Test updating existing player
        player = MagicMock(spec=Player)
        self.mock_model.player_list = {'Player1': player}
        self.controller.update_player()

        player.mosley_open_handicap = 10
        player.twisted_creek_handicap = 15
        player.save.assert_called_once()
        mock_update_player_list.assert_called_once()
        self.controller.clear_entry_fields.assert_called_once()

        # Test adding new player
        self.mock_model.player_list = {}
        new_player_instance = MagicMock(spec=Player)
        MockPlayer.return_value = new_player_instance
        self.controller.update_player()

        MockPlayer.assert_called_once_with('Player1', 15)
        new_player_instance.save.assert_called_once()
        mock_update_player_list.assert_called_once()
        self.controller.clear_entry_fields.assert_called_once()

        # Test deleting player
        self.mock_view.player_entry_frame.mosley_open_hc.get.return_value = ''
        self.mock_view.player_entry_frame.twisted_creek_hc.get.return_value = ''
        self.mock_model.player_list = {'Player1': player}
        self.controller.update_player()

        player.delete.assert_called_once()
        mock_update_player_list.assert_called_once()
        self.controller.clear_entry_fields.assert_called_once()

    def test_delete_player(self):
        player = MagicMock(spec=Player)
        self.mock_model.player_list = {'Player1': player}

        self.controller.delete_player('Player1')
        player.delete.assert_called_once()

        self.mock_model.player_list = {}
        with self.assertRaises(ValueError):
            self.controller.delete_player('Player1')

    def test_clear_entry_fields(self):
        self.controller.clear_entry_fields()
        self.mock_view.player_entry_frame.player.delete.assert_called_with(0, tk.END)
        self.mock_view.player_entry_frame.mosley_open_hc.delete.assert_called_with(0, tk.END)
        self.mock_view.player_entry_frame.twisted_creek_hc.delete.assert_called_with(0, tk.END)

if __name__ == '__main__':
    unittest.main()