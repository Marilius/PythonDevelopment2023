import unittest
from client.client.board import Board


class TestGameOver(unittest.TestCase):
    # детский мат
    @classmethod
    def setUpClass(cls):
        cls.board = Board()

    def test_GameOver(self):
        self.assertEqual(self.board.move('e', '2', 'e', '4'), 'e2-e4')
        self.assertEqual(self.board.move('e', '7', 'e', '5'), 'e7-e5')
        self.assertEqual(self.board.move('f', '1', 'c', '4'), 'Bf1-c4')
        self.assertEqual(self.board.move('b', '8', 'c', '6'), 'Nb8-c6')
        self.assertEqual(self.board.move('d', '1', 'h', '5'), 'Qd1-h5')
        self.assertEqual(self.board.move('g', '8', 'f', '6'), 'Ng8-f6')
        self.assertEqual(self.board.move('h', '5', 'f', '7'), 'Qh5xf7#')


class TestCheck(unittest.TestCase):
    # check test
    @classmethod
    def setUpClass(cls):
        cls.board = Board()

    def test_Check(self):
        self.assertEqual(self.board.move('e', '2', 'e', '4'), 'e2-e4')
        self.assertEqual(self.board.move('e', '7', 'e', '5'), 'e7-e5')
        self.assertEqual(self.board.move('d', '1', 'h', '5'), 'Qd1-h5')
        self.assertEqual(self.board.move('b', '8', 'c', '6'), 'Nb8-c6')
        self.assertEqual(self.board.move('h', '5', 'f', '7'), 'Qh5xf7+')


class TestKing(unittest.TestCase):
    # king test
    @classmethod
    def setUpClass(cls):
        cls.board = Board()

    def test_King(self):
        self.assertEqual(self.board.move('e', '2', 'e', '4'), 'e2-e4')
        self.assertEqual(self.board.move('e', '1', 'e', '2'), 'Ke1-e2')
        self.assertEqual(self.board.move('e', '2', 'e', '3'), 'Ke2-e3')
        self.assertEqual(self.board.move('e', '3', 'd', '4'), 'Ke3-d4')
        self.assertEqual(
            self.board.curr_possible_moves('d', '4'),
            [
                ('e', '5'),
                ('e', '3'),
                ('c', '4'),
                ('c', '5'),
                ('c', '3'),
                ('d', '5'),
                ('d', '3'),
            ],
        )


class TestRook(unittest.TestCase):
    # rook test
    @classmethod
    def setUpClass(cls):
        cls.board = Board()

    def test_Rook(self):
        self.assertEqual(self.board.move('a', '2', 'a', '4'), 'a2-a4')
        self.assertEqual(self.board.move('a', '1', 'a', '3'), 'Ra1-a3')
        self.assertEqual(self.board.move('a', '3', 'b', '3'), 'Ra3-b3')
        self.assertEqual(self.board.move('b', '3', 'b', '4'), 'Rb3-b4')
        self.assertEqual(
            self.board.curr_possible_moves('b', '4'),
            [
                ('c', '4'),
                ('d', '4'),
                ('e', '4'),
                ('f', '4'),
                ('g', '4'),
                ('h', '4'),
                ('b', '5'),
                ('b', '6'),
                ('b', '7'),
                ('b', '3'),
            ]
        )


class TestBishop(unittest.TestCase):
    # bishop test
    @classmethod
    def setUpClass(cls):
        cls.board = Board()

    def test_Bishop(self):
        self.assertEqual(self.board.move('e', '2', 'e', '4'), 'e2-e4')
        self.assertEqual(self.board.move('f', '1', 'c', '4'), 'Bf1-c4')
        self.assertEqual(self.board.move('c', '4', 'e', '2'), 'Bc4-e2')
        self.assertEqual(
            self.board.curr_possible_moves('e', '2'),
            [
                ('f', '3'),
                ('g', '4'),
                ('h', '5'),
                ('d', '3'),
                ('c', '4'),
                ('b', '5'),
                ('a', '6'),
                ('f', '1'),
            ]
        )


class TestPawnKnight(unittest.TestCase):
    # pawns and knight test
    @classmethod
    def setUpClass(cls):
        cls.board = Board()

    def test_PawnKnight(self):
        self.assertEqual(self.board.move('e', '2', 'e', '4'), 'e2-e4')
        self.assertEqual(self.board.move('e', '7', 'e', '5'), 'e7-e5')
        self.assertEqual(self.board.move('b', '1', 'c', '3'), 'Nb1-c3')
        self.assertEqual(self.board.move('a', '2', 'a', '4'), 'a2-a4')
        self.assertEqual(self.board.move('a', '4', 'a', '5'), 'a4-a5')
        self.assertEqual(self.board.move('a', '5', 'a', '6'), 'a5-a6')
        self.assertEqual(self.board.move('b', '7', 'a', '5'), None)
        self.assertEqual(self.board.curr_possible_moves('b', '2'), [('b', '3'), ('b', '4')])

if __name__ == '__main__':
    unittest.main()
