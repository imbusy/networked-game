import unittest

import game

class TestGame(unittest.TestCase):
    def test_hand_value(self):
        self.assertEqual(0, game.hand_value([]))
        self.assertEqual(10, game.hand_value([
            game.Card('diamonds', '10', False)
        ]))
        self.assertEqual(21, game.hand_value([
            game.Card('diamonds', '10', False),
            game.Card('diamonds', 'A', False)
        ]))
        self.assertEqual(12, game.hand_value([
            game.Card('diamonds', '10', False),
            game.Card('diamonds', 'A', False),
            game.Card('diamonds', 'A', False)
        ]))
