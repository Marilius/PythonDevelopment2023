"""
Chess board realisation.
"""
from pieces import BasePiece, NotPieceException


NUMS = '12345678'
LETTERS = 'abcdefgh'


class Board:
    """
    Board for chess game
    """
    def __init__(self) -> None:
        self.turn = 1
        self.curr_board = {}

        for i in 'abcdefgh':
            for j in '12345678':
                name, color = None, None

                if i in 'ah':
                    name = 'R'

                if i in 'bg':
                    name = 'N'

                if i in 'cf':
                    name = 'B'

                if i == 'd':
                    name = 'Q'

                if i == 'e':
                    name = 'K'

                if j in '27':
                    name = 'p'

                if j in '12':
                    color = 'w'

                if j in '78':
                    color = 'b'

                if name is None or color is None:
                    self.curr_board[(i, j)] = ' '
                else:
                    self.curr_board[(i, j)] = BasePiece(name=name, color=color)

                self.prev_board = self.curr_board.copy()

    @staticmethod
    def check(board: dict[tuple[str, str]]) -> list[str]:
        """checks if any king under the check

        :param board: game board
        :type board: dict[tuple[str, str]]
        :return: list of colors of kings under the check
        :rtype: list[str]
        """
        ans = []

        for pos in board.keys():
            if isinstance(board[pos], BasePiece):
                color = board[pos].color
                possible_moves = Board.get_possible_moves(board, *pos, ignore_fiter=True)
                for pos2 in possible_moves:
                    if isinstance(board[pos2], BasePiece):
                        if board[pos2].name == 'K' and board[pos2].color != color:
                            if board[pos2].color not in ans:
                                ans.append(board[pos2].color)

        return ans

    @staticmethod
    def game_over(board: dict[tuple[str, str]]) -> list[str]:
        """check if game is over

        :param board: game board
        :type board: dict[tuple[str, str]]
        :return: color of lost player
        :rtype: list[str]
        """
        if not Board.check(board):
            return []

        color = Board.check(board)[0]
        for pos in board.keys():
            if isinstance(board[pos], BasePiece):
                if board[pos].color == color:
                    if Board.get_possible_moves(board, *pos):
                        return []

        return [color]

    def curr_possible_moves(self, i: str, j: str) -> list[tuple[str, str]]:
        """possible moves for piece on (i, j) position on current board

        :param i: i piece pos
        :type i: str
        :param j: j piece pos
        :type j: str
        :return: list of possible piece's moves
        :rtype: list[tuple[str, str]]
        """
        return Board.get_possible_moves(self.curr_board, i, j)

    @staticmethod
    def get_possible_moves(board: dict[tuple[str, str]], i: str, j: str, ignore_fiter: bool = False) -> list[tuple[str, str]]:
        """returns listof possible moves for the piece on position (i, j) on passed board

        :param board: game board
        :type board: dict[tuple[str, str]]
        :param i: i piece pos
        :type i: str
        :param j: j piece pos
        :type j: str
        :param ignore_fiter: ignore check for the king check, defaults to False
        :type ignore_fiter: bool, optional
        :raises NotPieceException: i, j field is empty
        :return: list of possible moves
        :rtype: list[tuple[str, str]]
        """
        # TODO(marilius): en passant, рокировка
        if not isinstance(board[(i, j)], BasePiece):
            raise NotPieceException

        piece = board[(i, j)]
        piece_name = piece.name
        color = piece.color
        possible_moves = []

        match piece_name:
            case 'p':  # pawn
                if color == 'w':
                    d = 1
                else:
                    d = -1

                if not isinstance(board[(i, NUMS[NUMS.find(j) + d * 1])], BasePiece):
                    possible_moves.append((i, NUMS[NUMS.find(j) + d * 1]))

                    if not piece.moved and not isinstance(board[(i, NUMS[NUMS.find(j) + d * 2])], BasePiece):
                        possible_moves.append((i, NUMS[NUMS.find(j) + d * 2]))

                pos_j0 = NUMS.find(j) + d * 1

                pos_i0 = LETTERS.find(i) - 1
                if 0 <= pos_i0 <= 7:
                    if isinstance(board[(LETTERS[pos_i0], NUMS[pos_j0])], BasePiece):
                        if board[(LETTERS[pos_i0], NUMS[pos_j0])].color == 'b':
                            possible_moves.append((LETTERS[pos_i0], NUMS[pos_j0]))
                    # elif isinstance(self.prev_board[(LETTERS[pos_i0], NUMS[pos_j0])], BasePiece):
                        # if self.prev_board[(LETTERS[pos_i0], NUMS[pos_j0])].name == 'p':
                            # possible_moves.append((LETTERS[pos_i0], NUMS[pos_j0]))

                pos_i0 = LETTERS.find(i) + 1
                if 0 <= pos_i0 <= 7:
                    if isinstance(board[(LETTERS[pos_i0], NUMS[pos_j0])], BasePiece):
                        if board[(LETTERS[pos_i0], NUMS[pos_j0])].color == 'b':
                            possible_moves.append((LETTERS[pos_i0], NUMS[pos_j0]))
                    # elif isinstance(self.prev_board[(LETTERS[pos_i0], NUMS[pos_j0])], BasePiece):
                        # if self.prev_board[(LETTERS[pos_i0], NUMS[pos_j0])].name == 'p':
                            # possible_moves.append((LETTERS[pos_i0], NUMS[pos_j0]))

                # TODO(marilius): en passant

            case 'N':  # knight
                pos_i, pos_j = LETTERS.find(i), NUMS.find(j)

                for d0 in [-1, 1]:
                    for d1 in [-1, 1]:
                        if 0 <= pos_i + d0 * 1 <= 7 and 0 <= pos_j + d1 * 2 <= 7:
                            possible_moves.append((LETTERS[pos_i + d0 * 1], NUMS[pos_j + d1 * 2]))
                        if 0 <= pos_i + d0 * 2 <= 7 and 0 <= pos_j + d1 * 1 <= 7:
                            possible_moves.append((LETTERS[pos_i + d0 * 2], NUMS[pos_j + d1 * 1]))

            case 'B':  # bishop
                pos_i, pos_j = LETTERS.find(i), NUMS.find(j)

                for d in range(1, 8):
                    if 0 <= pos_i + d <= 7 and 0 <= pos_j + d <= 7:
                        possible_moves.append((LETTERS[pos_i + d], NUMS[pos_j + d]))
                        if isinstance(board[(LETTERS[pos_i + d], NUMS[pos_j + d])], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_i - d <= 7 and 0 <= pos_j + d <= 7:
                        possible_moves.append((LETTERS[pos_i - d], NUMS[pos_j + d]))
                        if isinstance(board[(LETTERS[pos_i - d], NUMS[pos_j + d])], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_i + d <= 7 and 0 <= pos_j - d <= 7:
                        possible_moves.append((LETTERS[pos_i + d], NUMS[pos_j - d]))
                        if isinstance(board[(LETTERS[pos_i + d], NUMS[pos_j - d])], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_i - d <= 7 and 0 <= pos_j - d <= 7:
                        possible_moves.append((LETTERS[pos_i - d], NUMS[pos_j - d]))
                        if isinstance(board[(LETTERS[pos_i - d], NUMS[pos_j - d])], BasePiece):
                            break

            case 'R':  # rook
                pos_i, pos_j = LETTERS.find(i), NUMS.find(j)
                for d in range(1, 8):
                    if 0 <= pos_i + d <= 7:
                        possible_moves.append((LETTERS[pos_i + d], j))
                        if isinstance(board[(LETTERS[pos_i + d], j)], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_i - d <= 7:
                        possible_moves.append((LETTERS[pos_i - d], j))
                        if isinstance(board[(LETTERS[pos_i - d], j)], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_j + d <= 7:
                        possible_moves.append((i, NUMS[pos_j + d]))
                        if isinstance(board[(i, NUMS[pos_j + d])], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_j - d <= 7:
                        possible_moves.append((i, NUMS[pos_j - d]))
                        if isinstance(board[(i, NUMS[pos_j - d])], BasePiece):
                            break

            case 'Q':  # Queen
                pos_i, pos_j = LETTERS.find(i), NUMS.find(j)
                for d in range(1, 8):
                    if 0 <= pos_i + d <= 7:
                        possible_moves.append((LETTERS[pos_i + d], j))
                        if isinstance(board[(LETTERS[pos_i + d], j)], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_i - d <= 7:
                        possible_moves.append((LETTERS[pos_i - d], j))
                        if isinstance(board[(LETTERS[pos_i - d], j)], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_j + d <= 7:
                        possible_moves.append((i, NUMS[pos_j + d]))
                        if isinstance(board[(i, NUMS[pos_j + d])], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_j - d <= 7:
                        possible_moves.append((i, NUMS[pos_j - d]))
                        if isinstance(board[(i, NUMS[pos_j - d])], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_i + d <= 7 and 0 <= pos_j + d <= 7:
                        possible_moves.append((LETTERS[pos_i + d], NUMS[pos_j + d]))
                        if isinstance(board[(LETTERS[pos_i + d], NUMS[pos_j + d])], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_i - d <= 7 and 0 <= pos_j + d <= 7:
                        possible_moves.append((LETTERS[pos_i - d], NUMS[pos_j + d]))
                        if isinstance(board[(LETTERS[pos_i - d], NUMS[pos_j + d])], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_i + d <= 7 and 0 <= pos_j - d <= 7:
                        possible_moves.append((LETTERS[pos_i + d], NUMS[pos_j - d]))
                        if isinstance(board[(LETTERS[pos_i + d], NUMS[pos_j - d])], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_i - d <= 7 and 0 <= pos_j - d <= 7:
                        possible_moves.append((LETTERS[pos_i - d], NUMS[pos_j - d]))
                        if isinstance(board[(LETTERS[pos_i - d], NUMS[pos_j - d])], BasePiece):
                            break

            case 'K':  # king
                pos_i, pos_j = LETTERS.find(i), NUMS.find(j)
                if 0 <= pos_i + 1 <= 7:
                    possible_moves.append((LETTERS[pos_i + 1], NUMS[pos_j]))
                    if 0 <= pos_j + 1 <= 7:
                        possible_moves.append((LETTERS[pos_i + 1], NUMS[pos_j + 1]))
                    if 0 <= pos_j - 1 <= 7:
                        possible_moves.append((LETTERS[pos_i + 1], NUMS[pos_j - 1]))

                if 0 <= pos_i - 1 <= 7:
                    possible_moves.append((LETTERS[pos_i - 1], NUMS[pos_j]))
                    if 0 <= pos_j + 1 <= 7:
                        possible_moves.append((LETTERS[pos_i - 1], NUMS[pos_j + 1]))
                    if 0 <= pos_j - 1 <= 7:
                        possible_moves.append((LETTERS[pos_i - 1], NUMS[pos_j - 1]))

                if 0 <= pos_j + 1 <= 7:
                    possible_moves.append((LETTERS[pos_i], NUMS[pos_j + 1]))
                if 0 <= pos_j - 1 <= 7:
                    possible_moves.append((LETTERS[pos_i], NUMS[pos_j - 1]))

                if not piece.moved:
                    # TODO(marilius): рокировка
                    ...

        def f(x: tuple[str, str]) -> bool:
            i, j = x

            # фигура того же цвета
            if isinstance(board[(i, j)], BasePiece):
                if board[(i, j)].color == color:
                    return False

            return True

        def under_check(x: tuple[str, str]) -> bool:
            i1, j1 = x

            next_board = board.copy()

            next_board[(i1, j1)] = next_board[(i, j)]
            next_board[(i, j)] = ' '

            if color in Board.check(next_board):
                return False

            return True

        possible_moves = list(filter(f, possible_moves))
        if not ignore_fiter:
            possible_moves = list(filter(under_check, possible_moves))

        ans = possible_moves
        # print(ans)
        return ans

    def move(self, i0: str, j0: str, i1: str, j1: str, promote: str = '') -> str:
        """move piece from (i0, j0) to (i1, j1)

        :param i0: i of starting position
        :type i0: str
        :param j0: j of starting position
        :type j0: str
        :param i1: i of ending position
        :type i1: str
        :param j1: j of ending position
        :type j1: str
        :param promote: promote pawn to chess piece, defaults to ''
        :type promote: str, optional
        :return: chess move notation
        :rtype: str
        """
        if (i1, j1) in self.get_possible_moves(self.curr_board, i0, j0):
            name0 = self.curr_board[(i0, j0)].piece_name

            if isinstance(self.curr_board[(i1, j1)], BasePiece):
                name1 = self.curr_board[(i1, j1)].piece_name
                sym = 'x'
            else:
                name1 = ''
                sym = '-'

            # TODO(marilius): Castling 0-0, 0-0-0

            self.prev_board = self.curr_board.copy()
            self.curr_board[(i1, j1)] = self.curr_board[(i0, j0)]
            self.curr_board[(i0, j0)] = ' '

            self.curr_board[(i1, j1)].move()

            check = ''
            if self.check(self.curr_board):
                check = '+'

            if self.game_over(self.curr_board):
                check = '#'

            return f'{name0}{i0}{j0}{sym}{name1}{i1}{j1}{check}{promote}'

    def print(self) -> None:
        """prints current board state
        """
        def f(x) -> int:
            if not isinstance(x, BasePiece):
                return 30
            if x.color == 'w':
                return 30
            else:
                return 37

        for j_pos, j in enumerate(reversed('12345678')):
            for i_pos, i in enumerate('abcdefgh'):
                s = self.curr_board[(i, j)]
                if (j_pos + i_pos) % 2:
                    print(f'\x1b[7;30;44m' + str(s) + '\x1b[0m', end='')
                else:
                    print(f'\x1b[5;30;44m' + str(s) + '\x1b[0m', end='')
            print()

# test = Board()
# test.print()
