import unittest
from client.client.pieces import BasePiece


class TestPawn(unittest.TestCase):
    # пешка в нотации
    @classmethod
    def setUpClass(cls):
        cls.piece = BasePiece('p', 'w')

    def test_PawnNotation(self):
        self.assertEqual(self.piece.piece_name, '')

if __name__ == '__main__':
    unittest.main()
