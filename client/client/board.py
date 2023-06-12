from pieces import BasePiece, NotPieceException


NUMS = '12345678'
LETTERS = 'abcdefgh'


class Board:
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
        return Board.get_possible_moves(self.curr_board, i, j)

    @staticmethod
    def get_possible_moves(board: dict[tuple[str, str]], i: str, j: str, ignore_fiter: bool = False) -> list[tuple[str, str]]:
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
        for j in reversed('12345678'):
            for i in 'abcdefgh':
                print(self.curr_board[(i, j)], end='')
            print()


test = Board()

# pawns and knight
# test.print()
# print(test.move('e', '2', 'e', '4'))
# test.print()
# print(test.move('e', '7', 'e', '5'))
# test.print()
# print(test.move('b', '1', 'c', '3'))
# test.print()
# print(test.move('a', '2', 'a', '4'))
# print(test.move('a', '4', 'a', '5'))
# print(test.move('a', '5', 'a', '6'))
# print(test.move('b', '7', 'a', '5'))
# test.print()
# test.curr_possible_moves('b', '2')

# bishop
# test.print()
# print(test.move('e', '2', 'e', '4'))
# test.print()
# print(test.move('f', '1', 'c', '4'))
# test.print()
# print(test.move('c', '4', 'e', '2'))
# test.print()
# print(test.curr_possible_moves('e', '2'))

# rook
# test.print()
# print(test.move('a', '2', 'a', '4'))
# test.print()
# print(test.move('a', '1', 'a', '3'))
# test.print()
# print(test.move('a', '3', 'b', '3'))
# test.print()
# print(test.move('b', '3', 'b', '4'))
# test.print()
# print(test.curr_possible_moves('b', '4'))


# king
# test.print()
# print(test.move('e', '2', 'e', '4'))
# test.print()
# print(test.move('e', '1', 'e', '2'))
# test.print()
# print(test.move('e', '2', 'e', '3'))
# test.print()
# print(test.move('e', '3', 'd', '4'))
# test.print()
# print(test.curr_possible_moves('d', '4'))

# check test
# test.print()
# print(test.move('e', '2', 'e', '4'))
# test.print()
# print(test.move('e', '7', 'e', '5'))
# test.print()
# print(test.move('d', '1', 'h', '5'))
# test.print()
# print(test.move('b', '8', 'c', '6'))
# test.print()
# print(test.move('h', '5', 'f', '7'))
# test.print()

# game over test, детский мат
# test.print()
# print(test.move('e', '2', 'e', '4'))
# test.print()
# print(test.move('e', '7', 'e', '5'))
# test.print()
# print(test.move('f', '1', 'c', '4'))
# test.print()
# print(test.move('b', '8', 'c', '6'))
# test.print()
# print(test.move('d', '1', 'h', '5'))
# test.print()
# print(test.move('g', '8', 'f', '6'))
# test.print()
# print(test.move('h', '5', 'f', '7'))
# test.print()
