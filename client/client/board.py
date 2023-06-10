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

    def get_possible_moves(self, i: str, j: str) -> list[tuple[str, str]]:
        # TODO(marilius): en passant, рокировка, шах
        if not isinstance(self.curr_board[(i, j)], BasePiece):
            raise NotPieceException

        piece = self.curr_board[(i, j)]
        piece_name = piece.name
        color = piece.color
        possible_moves = []

        match piece_name:
            case 'p':  # pawn
                if color == 'w':
                    d = 1
                else:
                    d = -1

                if not isinstance(self.curr_board[(i , NUMS[NUMS.find(j) + d * 1])], BasePiece):
                    possible_moves.append((i, NUMS[NUMS.find(j) + d * 1]))

                    if not piece.moved and not isinstance(self.curr_board[(i , NUMS[NUMS.find(j) + d * 2])], BasePiece):
                        possible_moves.append((i, NUMS[NUMS.find(j) + d * 2]))

                pos_j0 = NUMS.find(j) + d * 1

                pos_i0 = LETTERS.find(i) - 1
                if 0 <= pos_i0 <= 7:
                    if isinstance(self.curr_board[(LETTERS[pos_i0], NUMS[pos_j0])], BasePiece):
                        if self.curr_board[(LETTERS[pos_i0], NUMS[pos_j0])].color == 'b':
                            possible_moves.append((LETTERS[pos_i0], NUMS[pos_j0]))
                    # elif isinstance(self.prev_board[(LETTERS[pos_i0], NUMS[pos_j0])], BasePiece):
                        # if self.prev_board[(LETTERS[pos_i0], NUMS[pos_j0])].name == 'p':
                            # possible_moves.append((LETTERS[pos_i0], NUMS[pos_j0]))

                pos_i0 = LETTERS.find(i) + 1
                if 0 <= pos_i0 <= 7:
                    if isinstance(self.curr_board[(LETTERS[pos_i0], NUMS[pos_j0])], BasePiece):
                        if self.curr_board[(LETTERS[pos_i0], NUMS[pos_j0])].color == 'b':
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

            case 'K':  # king
                ...

            case 'B':  # bishop
                pos_i, pos_j = LETTERS.find(i), NUMS.find(j)

                for d in range(1, 8):
                    if 0 <= pos_i + d <= 7 and 0 <= pos_j + d <= 7:
                        possible_moves.append((LETTERS[pos_i + d], NUMS[pos_j + d]))
                        if isinstance(self.curr_board[(LETTERS[pos_i + d], NUMS[pos_j + d])], BasePiece):
                            break

                for d in range(1, 8):
                    if 0 <= pos_i - d <= 7 and 0 <= pos_j + d <= 7:
                        possible_moves.append((LETTERS[pos_i - d], NUMS[pos_j + d]))
                        if isinstance(self.curr_board[(LETTERS[pos_i - d], NUMS[pos_j + d])], BasePiece):
                            break
                
                for d in range(1, 8):
                    if 0 <= pos_i + d <= 7 and 0 <= pos_j - d <= 7:
                        possible_moves.append((LETTERS[pos_i + d], NUMS[pos_j - d]))
                        if isinstance(self.curr_board[(LETTERS[pos_i + d], NUMS[pos_j - d])], BasePiece):
                            break
                
                for d in range(1, 8):
                    if 0 <= pos_i - d <= 7 and 0 <= pos_j - d <= 7:
                        possible_moves.append((LETTERS[pos_i - d], NUMS[pos_j - d]))
                        if isinstance(self.curr_board[(LETTERS[pos_i - d], NUMS[pos_j - d])], BasePiece):
                            break

        def f(x) -> bool:
            i, j = x

            # фигура того же цвета
            if isinstance(self.curr_board[(i, j)], BasePiece):
                if self.curr_board[(i, j)].color == color:
                    return False

            return True

        possible_moves = list(filter(f, possible_moves))

        ans = possible_moves
        print(ans)
        return ans

    def move(self, i0: str, j0: str, i1: str, j1: str, promote: str = '') -> str:
        if (i1, j1) in self.get_possible_moves(i0, j0):
            name0 = self.curr_board[(i0, j0)].piece_name

            if isinstance(self.curr_board[(i1, j1)], BasePiece):
                name1 = self.curr_board[(i1, j1)].piece_name
                sym = 'x'
            else:
                name1 = ''
                sym = '-'

            # TODO(marilius): check
            check = ''

            # TODO(marilius): Castling 0-0, 0-0-0

            self.prev_board = self.curr_board.copy()
            self.curr_board[(i1, j1)] = self.curr_board[(i0, j0)]
            self.curr_board[(i0, j0)] = ' '

            self.curr_board[(i1, j1)].move()

            return f'{name0}{i0}{j0}{sym}{name1}{i1}{j1}{check}{promote}'

    def print(self) -> None:
        for j in reversed('12345678'):
            for i in 'abcdefgh':
                print(self.curr_board[(i, j)], end='')
            print()


test = Board()
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
# test.get_possible_moves('b', '2')

test.print()
print(test.move('e', '2', 'e', '4'))
test.print()
print(test.move('f', '1', 'c', '4'))
test.print()
print(test.move('c', '4', 'e', '2'))
test.print()
print(test.get_possible_moves('e', '2'))